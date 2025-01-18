# -*- coding: utf-8 -*-
# from odoo import http


# class PfConsumableStock(http.Controller):
#     @http.route('/pf_consumable_stock/pf_consumable_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pf_consumable_stock/pf_consumable_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pf_consumable_stock.listing', {
#             'root': '/pf_consumable_stock/pf_consumable_stock',
#             'objects': http.request.env['pf_consumable_stock.pf_consumable_stock'].search([]),
#         })

#     @http.route('/pf_consumable_stock/pf_consumable_stock/objects/<model("pf_consumable_stock.pf_consumable_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pf_consumable_stock.object', {
#             'object': obj
#         })

