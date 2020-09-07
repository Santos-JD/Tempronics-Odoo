from odoo import _,api, fields,models, tools

class ApiSettings(models.Model):
    _name = "api.settings.tempronics"
    _description = "Prueba"


    url = fields.Char('Pagina api')
    token = fields.Char('Token')
    company_id = fields.Many2one('res.company', 'Company',required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.user.company_id.id)

