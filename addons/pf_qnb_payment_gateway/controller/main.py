# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

import requests
from werkzeug import urls
from werkzeug.exceptions import Forbidden
import simplify
from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import html_escape
from odoo.addons.payment import utils as payment_utils
_logger = logging.getLogger(__name__)

class QnbController(http.Controller):
    _return_url = '/payment/qnb/return/'

    @http.route(_return_url, type='json', auth='public', methods=['GET', 'POST'], csrf=False)
    def qnb_return_from_checkout(self, **kwargs):
        _logger.info("data of qnb in controller %s", request.params)
        request_data = request.params
        if request_data:
            card_number = request_data.get('payment_data', {}).get('cardData', {}).get('cardNumber')
            exp_month = request_data.get('payment_data', {}).get('cardData', {}).get('month')
            exp_year = request_data.get('payment_data', {}).get('cardData', {}).get('year')
            card_cvc = request_data.get('payment_data', {}).get('cardData', {}).get('cardCode')

            transaction_ref = request_data.get('processing_data', {}).get('reference', {})
            partner_ref = request_data.get('processing_data', {}).get('partner_id', {})

            qnb_public_key = request_data.get('payment_data', {}).get('authData', {}).get('qnb_public_key', {})
            qnb_private_key = request_data.get('payment_data', {}).get('authData', {}).get('qnb_private_key', {})

            payment_amount = request_data.get('processing_data', {}).get('amount', {})
            description = "Payment of odoo"

            simplify.public_key = qnb_public_key
            simplify.private_key = qnb_private_key

            reference = request.env['payment.transaction'].search([('reference', '=', transaction_ref)])

            try:
                customer = request.env['res.partner'].search([('id', '=', partner_ref)])
                if customer:
                    name = customer.name
                    email = customer.email
                payment = simplify.Payment.create({
                    "amount" :payment_amount * 100,
                    "description" : "payment of odoo sale order " + transaction_ref + " with amount " + str(payment_amount) + " for " + name,
                    "reference": "odoo sale order " + transaction_ref, 
                    "card" : {
                        "name" : name,
                        "email" : email,
                        "number" : card_number,
                        "expMonth" : exp_month,
                        "cvc" : card_cvc,
                        "expYear" : exp_year
                    }
                })

                _logger.info("payment responce %s", payment)
                if payment:
                    payment_status = payment.paymentStatus
                    if payment_status == "APPROVED":
                        reference.write({'provider_reference':payment.id,'state':'done'})
                    else:
                        reference.write({'decline_reason':payment.declineReason,'provider_reference':payment.id,'state':'cancel'})
            except Exception as e:
                # Handle any potential errors
                _logger.error("An error occurred: %s", e)
                reference.write({'state': 'error'})
                        
        return request.redirect('/payment/status')
