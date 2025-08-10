from odoo import http
from odoo.http import request

class WebsiteController(http.Controller):

   @http.route('/api/feet/vehicles', type='http', auth='public', website=True)
   def hello_page(self):
       return {
            'status': 'success',
            'Message': 'Hello'
       }
