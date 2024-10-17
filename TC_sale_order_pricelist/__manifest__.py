{
    'name': 'Sale Order Pricelist',
    'summary': 'Adding pricelist option to all product in order lines',
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
        # 'security/ir.model.access.csv',
        'views/sale_order_lines_view.xml',
    ],
    'assets': {
    },
    'application': True,

}
