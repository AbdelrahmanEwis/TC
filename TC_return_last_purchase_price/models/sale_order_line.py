from odoo.exceptions import ValidationError

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            # check if the products have purchase bill it will return the last purchase price
            # elif the products doesnt have purchase bill it will return the cost
            # else it will trigger the default odoo function

            purchase_lines = self.env['purchase.order.line'].search([('product_id', '=', line.product_id.id)],
                                                                    order="id desc")
            last_price = purchase_lines[0].price_unit if len(purchase_lines) > 0 else 0
            if len(purchase_lines) > 0:
                line.price_unit = last_price
            elif len(purchase_lines) == 0:
                line.price_unit = line.product_template_id.standard_price
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            else:
                if line.qty_invoiced > 0 or (line.product_id.expense_policy == 'cost' and line.is_expense):
                    continue
                if not line.product_uom or not line.product_id:
                    line.price_unit = 0.0
                else:
                    line = line.with_company(line.company_id)
                    price = line._get_display_price()
                    line.price_unit = line.product_id._get_tax_included_unit_price_from_price(
                        price,
                        line.currency_id or line.order_id.currency_id,
                        product_taxes=line.product_id.taxes_id.filtered(
                            lambda tax: tax.company_id == line.env.company
                        ),
                        fiscal_position=line.order_id.fiscal_position_id,
                    )
