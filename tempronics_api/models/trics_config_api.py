from odoo.exceptions import UserError
from odoo import _,api, fields,models

class TricsConfigApi(models.Model):
    _name = "trics.config.api"
    _description = "Configuracion de URL para el Api de tempronics WEB"


    name = fields.Char('Nombre')
    url = fields.Char('URL Api')
    model = fields.Many2one('ir.model','Modelos')
    active = fields.Boolean('Accion')
    
