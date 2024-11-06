{
    'name': 'Pos Auto Cash Method',
    'summary': '',
    'author': "Tech Castle",
    'company': '"Tech Castle',
    'website': "",
    'version': '17.0.0.3',
    'category': "",
    'sequence': 1,
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_view.xml',
    ],
    'assets': {
        "point_of_sale._assets_pos": [
            'TC_pos_cash_default/static/src/**/*.js',
        ],
    },

    'application': True,

}
