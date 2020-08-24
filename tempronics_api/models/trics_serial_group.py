from odoo.exceptions import UserError
from odoo import _,api, fields,models, tools

class TricsSerialGroup(models.Model):
    _name="trics.serial.group"
    _description = "Grupo de seriales"
    

    name = fields.Chart('Nombre del grupo',index=True,required=True)

"""
class TricsSerialGroupRelation(models.Model):
    _name="trics.serial.group.relation"
    _description = "Relacion del grupo de seriales con el numero de ensamble"

    id_group = fields.Many2one('trics.serial.group',index=True,ondelete='cascade')
    material_product_tmpl_id = fields.Many2one('product.template','Producto ensamble',required=True)"""

