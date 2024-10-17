from odoo.exceptions import ValidationError

from odoo import api, fields, models
from odoo.tools import default_parser


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_list_id = fields.Many2one('product.pricelist')

    # updating price list for each line based on choosing
    # the pricelist in each line and clicking the button to update
    def update_price(self):
        for line in self:
            if line.price_list_id and line.product_id:
                pricelist = line.price_list_id
                product = line.product_id
                price = pricelist._get_product_price(product, 1.0, False)
                line.write({'price_unit': price})

    @api.onchange('product_id')
    def default_pricelist(self):
        if not self.product_id:
            self.price_list_id = self.order_id.pricelist_id.id
