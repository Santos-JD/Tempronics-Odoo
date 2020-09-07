from odoo.exceptions import UserError
from odoo import _,api, fields,models, tools
import requests

class TricsSerialGroup(models.Model):
    _name="trics.serial.group"
    _description = "Grupo de seriales"
    

    name = fields.Char('Category name',index=True,required=True)
    product_count = fields.Integer(
        '# Products', compute='_compute_product_count')
    
    def _compute_product_count(self):
        results = self.env['product.template'].read_group([('serial_group','in',self.ids)],['serial_group'],['serial_group'])
        group_data = dict((data['serial_group'][0], data['serial_group_count']) for data in results)
        for group in self:
            count = group_data.get(group.id)
            group.product_count = count


    @api.model
    def create(self,values):
        URL = 'http://127.0.0.1:88/api/odoo/serial_group.php'
        create = super(TricsSerialGroup,self).create(values)
        data = {}
        data['nombre'] = values['name']
        data['ID'] = create.id
        data['accion'] = 'create'
        POST = requests.post(URL,data = data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error en serial group \n %s" % (result['msj'])))
        return create

    def write(self,values):
        URL = 'http://127.0.0.1:88/api/odoo/serial_group.php'
        data = {}
        data['nombre'] = values['name']
        data['ID'] = self.id
        data['accion'] = 'write'
        POST = requests.post(URL,data = data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error en serial group modificar \n %s" % (result['msj'])))

        return super(TricsSerialGroup,self).write(values)

    def unlink(self):
        URL = 'http://127.0.0.1:88/api/odoo/serial_group.php'
        data = {}
        data['ID'] = self.id
        data['accion'] = 'unlink'
        POST = requests.post(URL,data = data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error en serial group eliminar \n %s" % (result['msj'])))

        return super(TricsSerialGroup,self).unlink()
            
            
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    serial_group = fields.Many2one('trics.serial.group','Serial Group',help="Selecciona un grupo")
    

           