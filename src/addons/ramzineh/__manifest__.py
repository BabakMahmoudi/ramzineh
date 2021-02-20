# -*- coding: utf-8 -*-
{
    'name': "ramzineh",

    'summary': """
        Ramzineh Extensions
        """,

    'description': """
        Ramzineh Extensions
    """,

    'author': "Gostareh Negar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/ir_sequence_data.xml',
        'wizards/ProductConfiguratorWizard_Views.xml',
        'views/Product_Views.xml',
        'views/SaleOrder_Views.xml',
        'views/PrintShop_Operation_Views.xml',
        # 'views/templates.xml',
        # 'views/action_views.xml',
        # 'views/branch_views.xml',
        # 'views/entry_views.xml',
        # 'views/file_views.xml',
        # 'views/issue_views.xml',
        # 'views/project_views.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
        # ''

    ],
    # 'qweb': ['static/src/xml/tree_view_button.xml'],
    'application': True,
    'installable': True,
}
