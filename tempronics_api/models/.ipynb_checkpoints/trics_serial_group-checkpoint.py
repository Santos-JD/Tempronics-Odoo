from odoo.exceptions import UserError
from odoo import _,api, fields,models, tools

class TricsSerialGroup(models.Model):
    _name="trics.serial.group"
    _description = "Grupo de seriales"
    

    name = fields.Char('Category name',index=True,required=True)
    product_count = fields.Integer(
        '# Products',
        help="The number of products under this category (Does not consider the children categories)")

"""
class TricsSerialGroupRelation(models.Model):
    _name="trics.serial.group.relation"
    _description = "Relacion del grupo de seriales con el numero de ensamble"

    id_group = fields.Many2one('trics.serial.group',index=True,ondelete='cascade')
    material_product_tmpl_id = fields.Many2one('product.template','Producto ensamble',required=True)"""

