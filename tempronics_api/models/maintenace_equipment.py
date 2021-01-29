import requests
import json
from odoo.exceptions import UserError
from odoo import _,api, fields,models

class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    @api.model
    def create(self,values):
        
        category = self.env['maintenance.equipment.category'].browse(values['category_id'])
        team = self.env['maintenance.team'].browse(values['maintenance_team_id'])
        
        dataEquipment = {} # Diccionario vacio, de lo que se mandara a la pagina
        
        dataEquipment['accion'] = 'create'
        dataEquipment['descripcion'] = values['name']
        dataEquipment['categoria'] = category.name
        dataEquipment['grupo'] = team.name
        dataEquipment['fecha_asig'] = values['assign_date']
        dataEquipment['notas'] = values['note']
        dataEquipment['vendedor_ref'] = values['partner_ref']
        dataEquipment['modelo'] = values['model']
        dataEquipment['serial'] = values['serial_no']
        dataEquipment['serial_interno'] = values['x_internal_serial']
        
        create = super(MaintenanceEquipment,self).create(values)
        fechacad = create.next_action_date
        
        dataEquipment['id_equip'] = create.id
        dataEquipment['fecha_cad'] = fechacad.strftime("%Y-%m-%d")
        
        #raise UserError(_("--Debug message--\n %s" % dataEquipment + "\n--End message--"))
        
        Api = self.env['trics.config.api'].RequestsHttpApi(self._inherit,dataEquipment)
        if not Api:
            raise UserError(_("Ocurrio un error al momento se generarlo para traceability\n %s" % result['msj']))

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