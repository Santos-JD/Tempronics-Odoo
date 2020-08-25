{
    'name': 'Tempronics API',
    'version': '12.0.1.0.0',
    'category': 'Manufacturing',
    'author': "Jose Monroy",
    'website': 'www.tempronics.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mrp',
        'product',
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/trics_mrp_bom_view.xml',
        'views/trics_serial_group_view.xml'
    ],
    'installable': True,
}
