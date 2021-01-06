from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TempronicsReport(models.Model):
    _name = 'tempronics.report'
    _description = 'Tempronics report'


    name = fields.Char(required=True)
    description = fields.Char(required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer('Color index', default=0)
    view_wiz = fields.Many2one('ir.ui.view','View')



    @api.multi
    def call_wizard(self):
        #raise UserError(_("Ocurrio un error al cambiar el estado a cancelado \n %s" % self))
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self.view_wiz.model,
            'view_id': self.view_wiz.id,
            'target': 'new'
        }