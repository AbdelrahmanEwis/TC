from odoo import models, api, fields
from datetime import datetime, timedelta


class AccountMove(models.Model):
    _inherit = 'account.move'

    item_count = fields.Float(compute="_compute_quantity_total", store=True)

    @api.depends('line_ids.quantity')
    def _compute_quantity_total(self):
        for rec in self:
            qty = rec.line_ids.mapped('quantity')
            rec.item_count = sum(qty)

    def action_post(self):
        # Call the original action post method
        record = super(AccountMove, self).action_post()

        # Process for each invoice
        for rec in self:
            lines = rec.line_ids
            inv_lines = rec.invoice_line_ids
            # Initialize income, outgoing, and balance
            income = 0.0
            outgoing = 0.0
            balance = 0.0
            statement_income = 0.0
            statement_outgoing = 0.0

            # Calculate income and outgoing based on move type
            if rec.move_type == 'out_invoice':
                income = rec.amount_total
            elif rec.move_type in ['in_invoice', 'in_refund']:
                outgoing = rec.amount_total

            # Retrieve the previous record if it exists
            sale_order_report = self.env['sale.order.report'].search([], order='id desc', limit=1)
            report_record = self.env['sale.order.report'].search([('move_id', '=', rec.id)], limit=1)
            account_statement_details = self.env['account.statement.details'].search([], order='id desc', limit=1)
            account_statement_record = self.env['account.statement.details'].search([('move_id', '=', rec.id)], limit=1)
            # Calculate balance
            if sale_order_report:
                balance = sale_order_report.balance + (income - outgoing)
            else:
                balance = income - outgoing

            for line in rec.invoice_line_ids:
                if rec.move_type == 'out_invoice':
                    statement_income = line.price_unit
                elif rec.move_type in ['in_invoice', 'in_refund']:
                    statement_outgoing = line.price_unit
                if account_statement_details:
                    statement_balance = account_statement_details.balance + (statement_income - statement_outgoing)
                else:
                    statement_balance = statement_income - statement_outgoing
                if account_statement_record:
                    account_statement_record.write({
                        'income': statement_income,
                        'outgoing': statement_outgoing,
                        'balance': abs(statement_balance),  # Calculate new balance
                        'state': rec.state,
                        'ref': rec.name,
                        'date': rec.invoice_date,
                    })

                else:
                    statement_vals = {
                        'date': rec.invoice_date,
                        'partner_id': line.partner_id.id,
                        'product_id': line.product_id.id,
                        'income': statement_income,
                        'outgoing': statement_outgoing,
                        'balance': abs(statement_balance),
                        'state': rec.state,
                        'ref': rec.name,
                        'move_id': rec.id,
                        'quantity': line.quantity,
                    }
                    self.env['account.statement.details'].create(statement_vals)
            if report_record:
                # Update existing record
                report_record.write({
                    'income': income,
                    'outgoing': outgoing,
                    'balance': abs(balance),  # Calculate new balance
                    'state': rec.state,
                    'ref': rec.name,
                    'date': rec.invoice_date,
                    'item_count': rec.item_count,
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
                    'item_count': rec.item_count,
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
                account_statement_record = self.env['account.statement.details'].search([('move_id', '=', move.id)],
                                                                                        limit=1)
                if account_statement_record:
                    account_statement_record.unlink()  # Delete the report record
                    # Recalculate balances for all remaining records
                    self._recalculate_balances()
                if report_record:
                    report_record.unlink()  # Delete the report record
                    # Recalculate balances for all remaining records
                    self._recalculate_balances()

        return res

    def _recalculate_balances(self):
        """Recalculate the balance, income, and outgoing for all sale.order.report records."""
        reports = self.env['sale.order.report'].search([])
        account_record = self.env['account.statement.details'].search([])
        for account_record in reports:
            # Fetch the corresponding move record
            previews_line = reports.filtered(lambda x: x.id > account_record.id)
            statement_income = 0
            statement_outgoing = 0
            if previews_line:
                # for line in account_record.move_id.line_ids:
                account_statement_record = previews_line[0]
                if account_statement_record.move_id.move_type == 'out_invoice':
                    statement_income = account_statement_record.move_id.price_unit
                elif account_statement_record.move_id.move_type in ['in_invoice', 'in_refund']:
                    statement_outgoing = account_statement_record.move_id.price_unit
                if account_statement_record:
                    statement_balance = account_record.balance + (statement_income - statement_outgoing)
                else:
                    statement_balance = statement_income - statement_outgoing
                account_statement_record.balance = statement_balance

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
