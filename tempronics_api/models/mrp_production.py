import requests
import json
from odoo.exceptions import UserError
from odoo import _,api, fields,models

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.model
    def create(self,values):
        api = self.env['trics.config.api'].getconfigapi(self._inherit)
            
        if not api.active: #Si no hay configuracion de API, ejecutara la funcion super
            #raise UserError(_("Entro en el if y ejecuta la funcion return super \n %s" % api))
            return super(MrpProduction,self).create(values)

        url = api.url
        dataProduction = {} # Diccionario vacio, de lo que se mandara a la pagina
        stock_ware = self.env['stock.warehouse.orderpoint'].search([('product_id','=',values['product_id'])]) #Obtenemos el qty_multiple en caso de tener....
        product = self.env['product.product'].browse(values['product_id']).default_code #obtiene el coodigo del producto para identificarlo en traceability
        qty = 1.0
        if stock_ware:
            qty = stock_ware.qty_multiple
        
        dataProduction['qty_multiple'] = qty
        dataProduction['product_qty'] = values['product_qty']
        dataProduction['date_planned_start'] = values['date_planned_start']
        dataProduction['product'] = product

        create = super(MrpProduction,self).create(values)
        
        dataProduction['name_production'] = values['name']
        post = requests.post(url, data = dataProduction)     #Hace la consulta por metodo POST
        textresult = post.text
        try:
            result = json.loads(textresult)
        except json.JSONDecodeError as e:
            raise UserError(_("Ocurrio un error al momento de generarlo para traceability\n %s \n %s" % (e,textresult)))

        """ El valor obtenido de la pagina lo convierte a un json para poder manipuarlo mas facilmente
            en caso que el texto no este en formato para convertir, lansara un error mas grande en odoo """
        
        if not result['success']:
            raise UserError(_("Ocurrio un error al momento de generarlo para traceability\n %s" % result['msj'])) #aqui mostrar el error que ocurrio y no continuara con 

        return create
    

