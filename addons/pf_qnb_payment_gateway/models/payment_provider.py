import logging

from odoo import _, fields, models
import json

# from odoo.addons.payment_paypal import const

from odoo.addons.pf_qnb_payment_gateway import const

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('qnb', "QNB")], ondelete={'qnb': 'set default'}
    )
    qnb_email = fields.Char(string="Email of QNB Account")
    qnb_public_key = fields.Text(string="Public Key of QNB")
    qnb_private_key = fields.Text(string="Private Key of QNB")

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'qnb').update({
            'support_express_checkout': True,
            'support_manual_capture': 'full_only',
            'support_refund': 'full_only',
            'support_tokenization': True,
        })

    def _get_supported_currencies(self):
        """ Override of `payment` to return the supported currencies. """
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'qnb':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in const.SUPPORTED_CURRENCIES
            )
        return supported_currencies
    
    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'qnb':
            return default_codes
        return const.DEFAULT_PAYMENT_METHODS_CODES
    
    def _qnb_get_inline_form_values(self):
        _logger.info("this is _qnb_get_inline_form_values %s", self)
        """ Return a serialized JSON of the required values to render the inline form. """
        self.ensure_one()

        inline_form_values = {
            'state': self.state,
            'public_key': self.qnb_public_key,
            'private_key': self.qnb_private_key,
        }
        _logger.info("Inline form values: %s", inline_form_values)
        return json.dumps(inline_form_values)


