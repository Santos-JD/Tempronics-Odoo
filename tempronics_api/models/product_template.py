import requests
from odoo.exceptions import UserError
from odoo import _,api, fields,models, tools

class productTemplate(models.Model):
    _inherit = 'product.template'

    
    def copy(self,default=None): #self, contiene los datos del ensamble que se va a compiar no del nuevo que se va generar.
        if default is None:
            default = {}
        if 'default_code' not in default: #Aqui creamos otro tipo de numerodeensamble que se insertara en sistema ade trazabilidad
            default['default_code'] = _("%s_copy") % self.default_code
            default['barcode'] =  _("%s_copy") % self.default_code
        copy = super(productTemplate,self).copy(default=default)
        return copy
        

    @api.model
    def create(self, values):
        api = self.env['trics.config.api'].getconfigapi(self._inherit)
        if not api.active:
            return super(productTemplate,self).create(values)

        url = api.url
        dataEnsamble = {}
        dataEnsamble['accion'] = 'create'
        dataEnsamble['descripcion'] = values['name']
        dataEnsamble['ensamble'] = values['default_code']
        dataEnsamble['category'] = values['categ_id']
        dataEnsamble['serie'] = 0
        if values.get('tracking') == 'serial':
            dataEnsamble['serie'] = 1
            dataEnsamble['serial_group'] = values['serial_group']
        create = super(productTemplate,self).create(values)
        if not create.categ_id.trics_sincronizar_ensambles:
            return create
        dataEnsamble['id'] = create.id
        POST = requests.post(url,data = dataEnsamble)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error al crear un nuevo producto en el sistema de produccion: \ %s" % (result['msj'])))
        return create



    def write(self,values):
        api = self.env['trics.config.api'].getconfigapi(self._inherit)
        if not api.active:
            return super(productTemplate,self).write(values)
        
        write = super(productTemplate,self).write(values)
        url = api.url
        dataEnsamble = {}
        dataEnsamble['accion'] = 'write'
        dataEnsamble['id'] = self.id
        dataEnsamble['ensamble'] = self.default_code
        dataEnsamble['descripcion'] = self.name
        dataEnsamble['category'] = self.categ_id.id
        dataEnsamble['active'] = self.active

        if self.tracking == 'serial':
            dataEnsamble['serie'] = 1
            dataEnsamble['serial_group'] = self.serial_group.id
        POST = requests.post(url,data = dataEnsamble)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Ocurrio un error al momento de actualiza el ensamble de produccion \n %s" % (result['msj'])))
        return write

    def unlink(self):
        api = self.env['trics.config.api'].getconfigapi(self._inherit)
        if not api.active:
            return super(productTemplate,self).unlink()

        url = api.url
        dataEnsamble = {}
        dataEnsamble['accion'] = 'unlink'
        dataEnsamble['id'] = self.id

        POST = requests.post(url,data = dataEnsamble)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Ocurrio un error al momento de eliminar el ensamble de produccion \n %s" % (result['msj'])))
        return super(productTemplate,self).unlink()
