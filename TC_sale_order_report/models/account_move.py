from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        # Call the original action post method
        record = super(AccountMove, self).action_post()

        # Process for each invoice
        for rec in self:
            # Initialize income, outgoing, and balance
            income = 0.0
            outgoing = 0.0
            balance = 0.0

            # Calculate income and outgoing based on move type
            if rec.move_type == 'out_invoice':
                income = rec.amount_total
            elif rec.move_type in ['in_invoice', 'in_refund']:
                outgoing = rec.amount_total

            # Retrieve the previous record if it exists
            sale_order_report = self.env['sale.order.report'].search([], order='id desc', limit=1)
            report_record = self.env['sale.order.report'].search([('move_id', '=', rec.id)], limit=1)
            # Calculate balance
            if sale_order_report:
                balance = sale_order_report.balance + (income - outgoing)
            else:
                balance = income - outgoing

            if report_record:
                # Update existing record
                report_record.write({
                    'income': income,
                    'outgoing': outgoing,
                    'balance': abs(balance),  # Calculate new balance
                    'state': rec.state,
                    'ref': rec.name,
                    'date': rec.invoice_date,
                })
            else:
                # Create a new record if it does not exist
                report_vals = {
                    'date': rec.invoice_date,
                    'partner_id': rec.partner_id.id,
                    'income': income,
                    'outgoing': outgoing,
                    'balance': abs(balance),
                    'state': rec.state,
                    'ref': rec.name,
                    'move_id': rec.id,
                }
                self.env['sale.order.report'].create(report_vals)

        return record

    def write(self, vals):
        # Call the super method to handle the write operation
        res = super(AccountMove, self).write(vals)

        # Check if the state is set to 'draft'
        for move in self:
            if 'state' in vals and vals['state'] == 'draft':
                # Find and unlink the corresponding sale.order.report record
                report_record = self.env['sale.order.report'].search([('move_id', '=', move.id)], limit=1)
                if report_record:
                    report_record.unlink()  # Delete the report record
                    # Recalculate balances for all remaining records
                    self._recalculate_balances()

        return res

    def _recalculate_balances(self):
        """Recalculate the balance, income, and outgoing for all sale.order.report records."""
        reports = self.env['sale.order.report'].search([])

        for report in reports:
            # Fetch the corresponding move record
            previews_line = reports.filtered(lambda x: x.id > report.id)
            income = 0
            outgoing = 0
            if previews_line:
                sale_order_report = previews_line[0]
                if sale_order_report.move_id.move_type == 'out_invoice':
                    income = sale_order_report.move_id.amount_total
                elif sale_order_report.move_id.move_type in ['in_invoice', 'in_refund']:
                    outgoing = sale_order_report.move_id.amount_total
                if sale_order_report:
                    balance = report.balance + (income - outgoing)
                else:
                    balance = income - outgoing
                sale_order_report.balance = balance

            #     another solution

            # if report == reports[-1] and len(reports) > 1:
            #     if reports[-1].move_id.move_type == 'out_invoice':
            #         income = reports[-1].move_id.amount_total
            #     elif reports[-1].move_id.move_type in ['in_invoice', 'in_refund']:
            #         outgoing = reports[-1].move_id.amount_total
            #     balance = reports[-2].balance + (income - outgoing)
            #     report.balance = balance
