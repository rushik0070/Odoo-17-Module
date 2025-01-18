# -*- coding: utf-8 -*-
{
    'name': "owl",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail','contacts','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/secquence.xml',
        'data/mail_template.xml',
        'views/todo_list.xml',
        'views/owl_task_report.xml',
        'views/chart.xml',
        'views/task.xml',
        'views/task_odoo.xml',
        'views/sale_order.xml'
        # 'views/sale_order_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets' : {
        'web.assets_backend' : [
            # 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.min.js'
            'https://cdn.jsdelivr.net/npm/chart.js',
            'owl/static/src/components/todo_list/todo_list.js',
            'owl/static/src/components/todo_list/todo_list.xml',
            'owl/static/src/components/todo_list/chart.js',
            'owl/static/src/components/todo_list/chart.xml',
            'owl/static/src/components/todo_list/chart.css',
            'owl/static/src/components/todo_list/task.js',
            'owl/static/src/components/todo_list/task.xml',
            'owl/static/src/components/todo_list/custom_widget.js',
            'owl/static/src/components/todo_list/custom_widget.xml',
            'owl/static/src/components/todo_list/custom_widget.xml',
            'owl/static/src/components/todo_list/test_widget.js',
            'owl/static/src/components/todo_list/test_widget.xml',
            # 'owl/static/src/components/todo_list/test_custom_widget.js',
            # 'owl/static/src/components/todo_list/test_custom_widget.xml',
        ],
    }
}

