
from datetime import datetime
from odoo import _,models, fields, api
from odoo.exceptions import UserError

class TempReportStockLocation(models.TransientModel):
    _name = "wizard.temp.report.stock.location"
    _description = "Report Stock Location"

    location = fields.Many2many('stock.location', 'temp_wh_loc_rel', 'wh', 'loc', string='Location')
    category = fields.Many2many('product.category', 'temp_categ_loc_rel', 'categ', 'loc', string='Category')
    document_name = fields.Char('Nombre del documento')
    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.temp.report.stock.location'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return self.env.ref('tempronics_report.stock_xlsx').report_action(self, data=datas)
        