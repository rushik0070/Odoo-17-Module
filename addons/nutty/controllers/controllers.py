# -*- coding: utf-8 -*-
# from odoo import http


# class Nutty(http.Controller):
#     @http.route('/nutty/nutty', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nutty/nutty/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nutty.listing', {
#             'root': '/nutty/nutty',
#             'objects': http.request.env['nutty.nutty'].search([]),
#         })

#     @http.route('/nutty/nutty/objects/<model("nutty.nutty"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nutty.object', {
#             'object': obj
#         })

