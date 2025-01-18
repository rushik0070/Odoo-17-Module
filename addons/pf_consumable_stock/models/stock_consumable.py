from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_active_stock = fields.Boolean(string="Active",default=False)
    is_master_stock = fields.Boolean(string="Fetch Stock from master product",default=False)
    stock_float = fields.Float(string="Main stock",default=0.0)
    master_stock_product = fields.Many2one(
        'product.template',
        string="Master Stock Product",
        domain="[('detailed_type', '=', 'consu'), ('is_master_stock', '=', False), ('id', '!=', id)]"  # Exclude current product
    )