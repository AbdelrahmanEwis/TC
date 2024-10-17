{
    'name': 'Sale Order Report',
    'summary': '',
    'author': "Tech Castle",
    'company': 'Tech Castle',
    'website': "",
    'version': '17.0.0.3',
    'category': "",
    'sequence': 1,
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_report_view.xml',
        'wizard/customer_payment_view.xml',
    ],
    'assets': {
    },
    'application': True,

}
