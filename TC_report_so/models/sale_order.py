from odoo import api, fields, models, _
from odoo.tools import formatLang

from datetime import timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    previous_balance = fields.Float(compute='_compute_previous_balance')
    payment_paid = fields.Float(compute='_compute_payment_paid')
    current_balance = fields.Float(compute='_compute_current_balance')

    @api.depends('partner_id')
    def _compute_previous_balance(self):
        for rec in self:
            rec.previous_balance = sum(rec.env['account.move'].search(
                [('partner_id', '=', rec.partner_id.id),
                 ('state', '=', 'posted'), ('id', 'not in', rec.invoice_ids.ids),
                 ('create_date', '<', rec.date_order)]).mapped('amount_residual'))

    @api.depends('invoice_ids')
    def _compute_payment_paid(self):
        invoices = self.mapped('invoice_ids')
        if len(invoices) > 0:
            total_invoices = invoices.mapped('amount_total')
            total_paid = invoices.mapped('amount_residual')
            self.payment_paid = sum(total_invoices) - sum(total_paid)
        else:
            self.payment_paid = 0.0

    @api.depends('amount_total', 'previous_balance', 'payment_paid')
    def _compute_current_balance(self):
        for rec in self:
            if rec.payment_paid:
                rec.current_balance = rec.previous_balance - (rec.payment_paid - rec.amount_total)
            else:
                rec.current_balance = rec.previous_balance + rec.amount_total
