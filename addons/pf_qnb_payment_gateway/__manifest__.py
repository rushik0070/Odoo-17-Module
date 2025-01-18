# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: QNB',
    'version': '2.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "QNB Payment Gateway",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['payment','pf_auto_install_library'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_qnb_templates.xml',
        'views/payment_transaction.xml',
        'data/payment_provider_data.xml',  # Depends on views/payment_razorpay_templates.xml
    ],
    # 'external_dependencies': {
    #     'python':[
    #         'matplotlib',
    #         'simplify',
    #         'simplifycommerce-sdk-python'
    #     ]
    # },
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            'pf_qnb_payment_gateway/static/src/scss/payment_qnb.scss',
            'pf_qnb_payment_gateway/static/src/**/*',
        ],
    },
}
