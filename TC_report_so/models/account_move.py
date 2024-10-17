from odoo import api, fields, models, _
from odoo.tools import formatLang

from datetime import timedelta


class AccountMove(models.Model):
    _inherit = 'account.move'

    previous_balance = fields.Float(compute='_compute_previous_balance')
    payment_paid = fields.Float(compute='_compute_payment_paid')
    current_balance = fields.Float(compute='_compute_current_balance')
    date_of_invoice = fields.Datetime(default=fields.Datetime.now)

    @api.depends('partner_id', 'create_date', 'date_of_invoice', 'amount_residual')
    def _compute_previous_balance(self):
        for rec in self:
            rec.previous_balance = sum(rec.env['account.move'].search(
                [('partner_id', '=', rec.partner_id.id),
                 ('state', '=', 'posted'), ('create_date', '<', rec.date_of_invoice)]).mapped('amount_residual'))

    @api.depends('amount_total', 'amount_residual')
    def _compute_payment_paid(self):
        for rec in self:
            rec.payment_paid = sum(rec.mapped('amount_total')) - sum(rec.mapped('amount_residual'))

    @api.depends('amount_total', 'previous_balance', 'payment_paid')
    def _compute_current_balance(self):
        for rec in self:
            rec.current_balance = rec.previous_balance + rec.amount_total - rec.payment_paid
