from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    order_line_count = fields.Integer(string='Order Line Count', compute='compute_line_count', store=True)
    num_qty = fields.Integer(string='Number Of Quantity',  compute='compute_line_count', store=True)
    def compute_line_count(self):
        for rec in self:
            rec.order_line_count = len(rec.order_line.mapped('id'))
            rec.num_qty = sum(rec.order_line.mapped('product_uom_qty'))