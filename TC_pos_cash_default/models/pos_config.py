# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    default_cash_method = fields.Many2one('pos.payment.method', string="Select Payment")

