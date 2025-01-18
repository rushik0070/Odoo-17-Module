from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _check_stock_quantity(self):
        # Create a dictionary to store the total ordered quantity per product template
        stock_check = {}

        # Iterate over the order lines to aggregate quantities for each product template
        for line in self.order_line:
            # Get the corresponding product template for the product variant
            product_template = line.product_id.product_tmpl_id

            # Only check for consumable products
            if line.product_id.type == 'consu' and line.product_id.is_active_stock:  # 'consu' stands for consumable
                # Accumulate the quantities for each product template
                if product_template not in stock_check:
                    stock_check[product_template] = 0
                stock_check[product_template] += line.product_uom_qty
        
        _logger.info("stock_check %s",stock_check)

        # Now check if any of the consumable product templates exceed their stock_float
        for product_template, total_qty in stock_check.items():
            if product_template.is_master_stock:
                stock_float = product_template.master_stock_product.stock_float
            else:
                stock_float = product_template.stock_float
            if total_qty > stock_float:
                raise UserError(
                    f"The total quantity for {product_template.name} exceeds the available stock of {stock_float}."
                )

    def _update_stock_quantity(self):
        # Deduct the ordered quantity from stock_float for consumable products only
        for line in self.order_line:
            if line.product_id.type == 'consu' and line.product_id.is_active_stock:  # Only process consumables
                product_template = line.product_id.product_tmpl_id

                if product_template.is_master_stock:
                    product_template = line.product_id.master_stock_product

                # Deduct the ordered quantity
                product_template.stock_float -= line.product_uom_qty

                # Ensure that stock_float doesn't go negative
                if product_template.stock_float < 0:
                    product_template.stock_float = 0

                # Save the updated stock_float
                product_template.sudo().write({
                    'stock_float': product_template.stock_float,
                })

    def action_confirm(self):
        # Check stock availability before confirming the order
        self._check_stock_quantity()

        # Proceed with the original action_confirm functionality
        res = super(SaleOrder, self).action_confirm()

        # # Deduct stock after the order is confirmed
        self._update_stock_quantity()

        return res
