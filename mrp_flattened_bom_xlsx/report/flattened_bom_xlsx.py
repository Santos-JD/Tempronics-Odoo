# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class FlattenedBomXlsx(models.AbstractModel):
    _name = 'report.mrp_flattened_bom_xlsx.flattened_bom_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_totals(self,id,locations):
        total = 0
        totals = []
        product = self.env['product.product'].search([('product_tmpl_id', '=', id)])
        for location in locations:
            virtual_available = product.with_context({'location': location.id}).virtual_available
            outgoing_qty = product.with_context({'location': location.id}).outgoing_qty
            incoming_qty = product.with_context({'location': location.id}).incoming_qty
            available_qty = virtual_available + outgoing_qty - incoming_qty
            total = total + available_qty 
            totals.append(available_qty)
        totals.append(total)
        return totals

    def print_flattened_bom_lines(self, bom, requirements, sheet, row, locations):
        i = row
        sheet.write(i, 0, bom.product_tmpl_id.name or '')
        sheet.write(i, 1, bom.code or '')
        sheet.write(i, 2, bom.display_name or '')
        sheet.write(i, 3, bom.product_qty)
        sheet.write(i, 4, bom.product_uom_id.name or '')
        totals = self.get_totals(bom.product_tmpl_id.id,locations)
        
        col_wt = 5
        for l in range(0,len(totals)):
            sheet.write(i,col_wt,totals[l])
            col_wt += 1


        #sheet.write(i, 5, bom.code or '')
        i += 1
        for product, total_qty in requirements.items():
            sheet.write(i, 1, product.default_code or '')
            sheet.write(i, 2, product.display_name or '')
            sheet.write(i, 3, total_qty or 0.0)
            sheet.write(i, 4, product.uom_id.name or '')
            #sheet.write(i, 5, product.code or '')
            totals = self.get_totals(product.product_tmpl_id.id,locations)
            col_wt = 5
            for l in range(0,len(totals)):
                sheet.write(i,col_wt,totals[l])
                col_wt += 1

            i += 1
        return i

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 11.0'})
        sheet = workbook.add_worksheet(_('Flattened BOM'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(1, 2, 20)
        sheet.set_column(3, 3, 40)
        sheet.set_column(4, 6, 20)
        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})

        locations = self.env['stock.location'].search([('id', 'in', [13, 86, 18, 12, 21])])

        sheet_title = [_('BOM Name'),
                       _('Product Reference'),
                       _('Product Name'),
                       _('Quantity'),
                       _('UM'),
                       ]
        for location in locations:
            sheet_title.append(_(location.display_name))

        sheet_title.append(_('Total'))
        #sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.write_row(0,0,"Reporte # 2: Requerimiento de Materiales por Numero de Parte",title_style)
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        i = 2

        for o in objects:
            # We need to calculate the totals for the BoM qty and UoM:
            starting_factor = o.product_uom_id._compute_quantity(
                o.product_qty, o.product_tmpl_id.uom_id, round=False)
            totals = o._get_flattened_totals(factor=starting_factor)
            i = self.print_flattened_bom_lines(o, totals, sheet, i, locations)
