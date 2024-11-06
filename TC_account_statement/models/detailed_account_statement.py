from odoo.exceptions import ValidationError

from odoo import api, fields, models


class DetailedAccountStatement(models.Model):
    _name = 'account.statement.details'

    date = fields.Date(string="Date")
    partner_id = fields.Many2one('res.partner', string="Customer")
    ref = fields.Char('Reference')
    balance = fields.Float()
    outgoing = fields.Float(string="Outgoing")
    income = fields.Float(string="Income")
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ])
    move_id = fields.Many2one('account.move')
    quantity = fields.Float()
    product_id = fields.Many2one('product.product', string="Product")
