# -*- coding: utf-8 -*-
# from odoo import http


# class ComptaMarche(http.Controller):
#     @http.route('/compta__marche/compta__marche/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/compta__marche/compta__marche/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('compta__marche.listing', {
#             'root': '/compta__marche/compta__marche',
#             'objects': http.request.env['compta__marche.compta__marche'].search([]),
#         })

#     @http.route('/compta__marche/compta__marche/objects/<model("compta__marche.compta__marche"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('compta__marche.object', {
#             'object': obj
#         })
