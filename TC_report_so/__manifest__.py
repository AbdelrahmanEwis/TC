{
    'name': 'Report SO',
    'summary': 'Adding total customer payment in  Sale Order Report and Invoice Report ',
    'author': "Tech Castle",
    'company': 'Tech Castle',
    'website': "",
    'version': '17.0.0.3',
    'category': "",
    'sequence': 1,
    'depends': [
        'base',
        'sale',
        'account',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'reports/account_move_report.xml',
        'reports/sale_order_report.xml',
    ],
    'assets': {
    },
    'application': True,

}
