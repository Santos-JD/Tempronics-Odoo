
from datetime import datetime
from odoo import _,models, fields, api

class TempReportStockLocation(models.TransientModel):
    _name = "wizard.temp.report.stock.location"
    _description = "Report Stock Location"

    #Se tiene que hacer dinamico esta parte
    _default_location = [13, 86, 18, 12, 21]
    _default_category = [4]
    location = fields.Many2many('stock.location', 'wh_loc_rel', 'wh', 'loc', string='Location', default=_default_location)
    category = fields.Many2many('product.category', 'categ_loc_rel', 'categ', 'loc', string='Category',default=_default_category)

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
            return self.env.ref('export_stockinfo_xls.stock_xlsx').report_action(self, data=datas)