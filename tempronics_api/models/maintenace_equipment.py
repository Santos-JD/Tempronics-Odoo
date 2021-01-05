import requests
import json
from odoo.exceptions import UserError
from odoo import _,api, fields,models

class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    @api.model
    def create(self,values):
        UserError(_("Ocurrio un error al momento se generarlo para traceability\n %s" % values))
        dataEquipment = {} # Diccionario vacio, de lo que se mandara a la pagina
        
        dataEquipment['accion'] = 'create'
        dataEquipment['qty_multiple'] = qty
        dataEquipment['product_qty'] = values['product_qty']
        dataEquipment['date_planned_start'] = values['date_planned_start']
        dataEquipment['product'] = product
        create = super(MaintenanceEquipment,self).create(values)
        dataEquipment['name_production'] = values['name']
        dataEquipment['id_bom'] = values['bom_id']
        
        Api = self.env['trics.config.api'].RequestsHttpApi(self._inherit,dataEquipment)
        if not Api:
            raise  #aqui mostrar el error que ocurrio y no continuara con 

        return create

    def write(self,values):
        #{'state': 'cancel', 'is_locked': True}

        if values.get('state') == 'cancel' and values.get('is_locked'):
            dataProduccion = {}
            dataProduccion['accion'] = 'unlink' # se mandara a eliminar, por que no nos servira tener el registro, si ya se encuentra en Odoo
            dataProduccion['name_production'] = self.name
            Api = self.env['trics.config.api'].RequestsHttpApi(self._inherit,dataProduccion)
            if not Api:
                raise UserError(_("Ocurrio un error al cambiar el estado a cancelado"))

        return super(MaintenanceEquipment,self).write(values)