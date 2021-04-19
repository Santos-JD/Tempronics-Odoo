{
    'name': 'Tempronics Studio',
    'version': '12.0.0.0.0',
    'summary': 'Internal modifications for Odoo',
    'author': "Jose Monroy",
    'website': 'https://www.tempronics.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mrp',
        'product',
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_classification_view.xml',
        'views/product_template_classification_view.xml'
        
    ],
    'application': True,
}