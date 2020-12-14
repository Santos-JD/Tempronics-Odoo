# -*- coding: utf-8 -*-

import datetime
from datetime import datetime
import pytz
from odoo import models

class StockReportXls(models.AbstractModel):
    _name = 'report.export_stockinfo_xls.stock_report_xls.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_location(self, data):
        wh = data.location.mapped('id')
        obj = self.env['stock.location'].search([('id', 'in', wh)])
        l1 = []
        l2 = []
        for j in obj:
            l1.append(j.name)
            l2.append(j.id)
        return l1, l2

    def generate_xlsx_report(self, workbook, data, lines):
        d = lines.category
        get_location = self.get_location(lines)
        count = len(get_location[0]) + 10
        comp = self.env.user.company_id.name
        sheet = workbook.add_worksheet('Stock Info')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
        font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
        font_size_8_r = workbook.add_format({'font_size': 8, 'align': 'right'})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        format1.set_border()
        
        red_mark.set_align('center')
        w_house = ', '
        cat = ', '
        c = []
        d1 = d.mapped('id')
        sheet.merge_range(0, 0, 0, 3, 'Reporte # 1: Master Inventory Data', format4)
        if d1:
            for i in d1:
                c.append(self.env['product.category'].browse(i).name)
            cat = cat.join(c)
            sheet.merge_range(1, 0, 1, 1, 'Category(s) : ', format4)
            sheet.merge_range(1, 2, 1, 3 + len(d1), cat, format4)
        
        user = self.env['res.users'].browse(self.env.uid)
        tz = pytz.timezone(user.tz)
        time = pytz.utc.localize(datetime.now()).astimezone(tz)
        sheet.merge_range('A4:G4', 'Report Date: ' + str(time.strftime("%Y-%m-%d %H:%M %p")), format1)
        sheet.merge_range(4, 11, 4, count, 'Locations', format1)
        sheet.merge_range('A5:G5', 'Product Information', format11)
        w_col_no = 10
        w_col_no1 = 11
        for i in get_location[0]:
            sheet.write(5, w_col_no1, i, format11)
            w_col_no1 = w_col_no1 + 1
        format21.set_border()
        sheet.write(5, 0, 'SKU', format21)
        sheet.merge_range(5, 1, 5, 3, 'Name', format21)
        sheet.merge_range(5, 4, 5, 5, 'Category', format21)
        sheet.write(5, 6, 'Cost Price', format21)
        sheet.write(5, 7, 'UM', format21) #unidad de medida
        sheet.write(5, 8, 'LT', format21) #LiteTime
        sheet.write(5, 9, 'Supplier', format21)
        sheet.write(5, 10, 'Origen', format21)
        sheet.write(5,count+1,'Total',format21)
        #sheet.write(5,count+2,'Reserved',format21)
        #sheet.write(5,count+3,'BAL',format21)

        prod_row = 6
        prod_col = 0
        font_size_8.set_border()
        font_size_8_l.set_border()
        font_size_8_r.set_border()
        for i in get_location[1]:
            get_line = self.get_lines(d, i)
            for each in get_line:
                sheet.write(prod_row, prod_col, each['sku'], font_size_8)
                sheet.merge_range(prod_row, prod_col + 1, prod_row, prod_col + 3, each['name'], font_size_8_l)
                sheet.merge_range(prod_row, prod_col + 4, prod_row, prod_col + 5, each['category'], font_size_8_l)
                sheet.write(prod_row, prod_col + 6, each['cost_price'], font_size_8_r)
                sheet.write(prod_row, prod_col + 7, each['um'], font_size_8_r)
                sheet.write(prod_row, prod_col + 8, each['lt'], font_size_8_r)
                sheet.write(prod_row, prod_col + 9, each['vendor'], font_size_8_r)
                sheet.write(prod_row, prod_col + 10, each['country'], font_size_8_r)
                prod_row = prod_row + 1
            break
        prod_row = 6
        prod_col = 11
        red_mark.set_border()
        
        for i in get_location[1]:
            get_line = self.get_lines(d, i)
            for each in get_line:
                if each['available'] < 0:
                    sheet.write(prod_row, prod_col, each['available'], red_mark)
                else:
                    sheet.write(prod_row, prod_col, each['available'], font_size_8)
                prod_row = prod_row + 1
            prod_row = 6
            prod_col = prod_col + 1


            # continue

    def get_lines(self, data, location):
        lines = []
        categ_id = data.mapped('id')
        if categ_id:
            categ_products = self.env['product.product'].search([('categ_id', 'in', categ_id)])

        else:
            categ_products = self.env['product.product'].search([])
        product_ids = tuple([pro_id.id for pro_id in categ_products])
    
        for obj in categ_products:
            virtual_available = obj.with_context({'location': location}).virtual_available
            outgoing_qty = obj.with_context({'location': location}).outgoing_qty
            incoming_qty = obj.with_context({'location': location}).incoming_qty
            available_qty = virtual_available + outgoing_qty - incoming_qty
            vendor = 'N/A'
            lt = 'N/A'
            vendorname = 'N/A'
            country = 'N/A'
            if(obj.seller_ids):
                vendorname = obj.seller_ids[0].name.name
                lt = obj.seller_ids[0].delay
                country = obj.seller_ids[0].name.country_id.code

            vals = {
                'sku': obj.default_code,
                'name': obj.name,
                'category': obj.categ_id.name,
                'cost_price': obj.standard_price,
                'lt': lt,
                'um': obj.uom_id.name,
                'vendor': vendorname,
                'country': country,
                'available': available_qty,
                
            }
            lines.append(vals)
        return lines



