# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import time
from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo.addons.payment import utils as payment_utils

from odoo import _, fields, api, models
from odoo.exceptions import UserError, ValidationError
from werkzeug.urls import url_encode, url_join

from werkzeug import urls
# from odoo.addons.pf_qnb_payment_gateway.const import PAYMENT_STATUS_MAPPING
from odoo.addons.pf_qnb_payment_gateway.controller.main import QnbController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    qnb_type = fields.Char(string="QNB Transaction Type")
    decline_reason = fields.Char(string="QNB Payment Decline Reason")

    # operation = fields.Selection(
    #     selection_add=[('online_direct', "Online direct payment")],
    #     default='online_direct',
    # )
    
    def _get_specific_processing_values(self, processing_values):
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'qnb':
            return res
             
        # return self._get_specific_rendering_values(self)
        base_url = self.provider_id.get_base_url()
        return {
            'return_url': url_join(
                base_url,
                f'{QnbController._return_url}?{url_encode({"reference": self.reference})}',
            ),
        }

        

        


   