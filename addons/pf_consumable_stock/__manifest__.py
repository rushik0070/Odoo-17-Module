# -*- coding: utf-8 -*-
{
    'name': "Stock management for consumable product",

    'summary': "Stock management for consumable product",

    'description': """
Stock management for consumable product
    """,

    'author': "Prefortune Technologies LLP",
    'website': "https://www.prefortune.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_consumable.xml',
    ],
}

