{
    "name": 'properties',
    "author": 'mohamed',
    "category": 'sales',
    "sequence": 1,
    "depends": ['base', 'sale_management', 'account', 'mail'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/property_owner_view.xml',
        'views/tags_view.xml',
        'views/sale_order_inherit_view.xml',
        'reports/property_report.xml',
    ],
    "application": True,
}
