from . import models
from . import controller

import subprocess
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

from odoo.addons.payment import setup_provider, reset_payment_provider

def pre_init_hook(env):
    _logger.info("THis is Preinit hook call")
    try:
        matplotlib = subprocess.run(["pip3", 'install', "matplotlib"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        _logger.info("THis is install matplotlib")
        simplify = subprocess.run(["pip3", 'install', "simplify"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        _logger.info("THis is install simplify")
        simplifycommerce_sdk_python = subprocess.run(["pip3", 'install', "simplifycommerce-sdk-python"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        _logger.info("THis is install simplifycommerce_sdk_python")
        # raise UserError(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        # Handle errors here
        _logger.info(f"Error: {e.stderr.decode('utf-8')}")
        raise UserError(f"Error: {e.stderr.decode('utf-8')}")
        

def post_init_hook(env):
    setup_provider(env, 'qnb')


def uninstall_hook(env):
    reset_payment_provider(env, 'qnb')