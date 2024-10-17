{
    'name': 'User Access',
    'summary': 'user access log ',
    'author': "Tech Castle",
    'company': 'Tech Castle',
    'website': "",
    'version': '17.0.0.3',
    'category': "",
    'sequence': 1,
    'depends': [
        'base',
        'sale_management',
        'product',
        'account',
        'mail',
        'contacts',
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
    ],
    'assets': {
    },
    'application': True,

}
