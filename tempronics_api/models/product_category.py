import requests
from odoo.exceptions import UserError
from odoo import _,api, fields,models, tools

class productCategory(models.Model):
    _inherit = 'product.category'

    trics_sincronizar_ensambles = fields.Boolean('Sincronizar a Sistema de Produccion (Ensambles)')


    @api.model
    def create(self, values):
        api = self.env['trics.config.api'].getconfigapi(self._inherit)
        if not api.active:
            return super(productCategory,self).create(values)
        url = api.url
        data = {}
        create = super(productCategory,self).create(values)
        data['accion'] = 'create'
        data['id'] = self.id
        data['name'] = self.name
        POST = requests.post(url,data = data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error al crear una nueva categoria en el sistema de produccion: \ %s" % (result['msj'])))
        return create

    def write(self,values):
        api = self.env['trics.config.api'].getconfigapi(self._inherit)
        if not api.active:
            return super(productCategory,self).write(values)
        url = api.url
        data = {}
        write = super(productCategory,self).write(values)
        data['accion'] = 'write'
        data['id'] = self.id
        data['name'] = self.name
        POST = requests.post(url,data = data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error al actualizar categoria en el sistema de produccion: \ %s" % (result['msj'])))
        return write
    
    def unlink(self):
        api = self.env['trics.config.api'].getconfigapi(self._inherit)
        if not api.active:
            return super(productCategory,self).unlink()
        url = api.url
        data = {}
        data['accion'] = 'unlink'
        data['id'] = self.id
        POST = requests.post(url,data = data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error al borrar categoria en el sistema de produccion: \ %s" % (result['msj'])))
        return super(productCategory,self).unlink()