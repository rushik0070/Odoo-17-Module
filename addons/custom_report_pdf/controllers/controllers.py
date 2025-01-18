# -*- coding: utf-8 -*-
# from odoo import http


# class CustomReportPdf(http.Controller):
#     @http.route('/custom_report_pdf/custom_report_pdf', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_report_pdf/custom_report_pdf/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_report_pdf.listing', {
#             'root': '/custom_report_pdf/custom_report_pdf',
#             'objects': http.request.env['custom_report_pdf.custom_report_pdf'].search([]),
#         })

#     @http.route('/custom_report_pdf/custom_report_pdf/objects/<model("custom_report_pdf.custom_report_pdf"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_report_pdf.object', {
#             'object': obj
#         })

