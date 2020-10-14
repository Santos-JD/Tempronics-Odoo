import requests
from odoo.exceptions import UserError
from odoo import _,api, fields,models, tools

class TricsMrpBom(models.Model):
    _name="trics.mrp.bom"
    _rec_name = 'material_product_tmpl_id'
    _order = "id"
    _description = "Traceability BOMs (rutas)"
    trics_bom_id = fields.Many2one('mrp.bom',index=True,ondelete='cascade')
    material_product_tmpl_id = fields.Many2one('product.template','Product(material)',required=True)
    rxp_qty = fields.Integer('Ruta por pieza',default=1,required=True,help="Ruta por pieza")
    lotes_qty = fields.Integer('Cantidad por lote',default=1,required=True,help="Cantidad por lote")



    @api.model
    def create(self,values):
        api = self.env['trics.config.api'].getconfigapi(self._name)
        if not api.active:
            return super(TricsMrpBom,self).create(values)
        url = api.url
        #Numero de ensamble Primario
        #Material numero de ensamble secundario
        #rxp
        #lotes
        #product = self.env['product.template']
        """
        Error en crear una ruta:
        {'rxp_qty': 1, 'lotes_qty': 580, 'material_product_tmpl_id': 728, 'trics_bom_id': 986}
        """
        create = super(TricsMrpBom,self).create(values)
        data = {}
        data['accion'] = 'create'
        data['numeroenmsable'] = create.trics_bom_id.product_tmpl_id.default_code
        data['material'] = create.material_product_tmpl_id.default_code
        data['rxp'] = create.rxp_qty
        data['lotes'] = create.lotes_qty
        data['id'] = create.id
        POST = requests.post(url,data=data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error en crear una ruta: \n %s " % (result['msj'])))
        return create
        
    def write(self,values):
        api = self.env['trics.config.api'].getconfigapi(self._name)
        if not api.active:
            return super(TricsMrpBom,self).write(values)
        url = api.url
        write = super(TricsMrpBom,self).write(values)
        data = {}
        data['accion'] = 'write'
        data['id'] = self.id
        data['numeroensamble'] = self.trics_bom_id.product_tmpl_id.default_code
        data['material'] = self.material_product_tmpl_id.default_code
        data['rxp'] = self.rxp_qty
        data['lotes'] = self.lotes_qty
        POST = requests.post(url,data = data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error al actualizar datos en ruta: \n %s" % (result['msj'])))
        return write


    def unlink(self):
        api = self.env['trics.config.api'].getconfigapi(self._name)
        if not api.active:
            return super(TricsMrpBom,self).unlink()
        url = api.url
        unlink = super(TricsMrpBom,self).unlink()
        data = {}
        data['accion'] = 'unlink'
        data['id'] = self.id
        POST = requests.post(url,data=data)
        result = POST.json()
        if not result['success']:
            raise UserError(_("Error al eliminar la ruta: \n %s" % (result['msj'])))
        return unlink

class MrpBom(models.Model):
    _inherit = ['mrp.bom']
    trics_id = fields.One2many('trics.mrp.bom','trics_bom_id')


    def unlink(self):
        values = self.env['trics.mrp.bom'].search([('trics_bom_id','=',self.id)])
        for value in values:
            value.unlink()

        u = super(MrpBom,self).unlink()
        return u
        
