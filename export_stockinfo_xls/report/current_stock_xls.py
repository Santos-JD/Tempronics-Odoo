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
            l1.append(j.display_name)
            l2.append(j.id)
        return l1, l2

    def generate_xlsx_report(self, workbook, data, lines):
        d = lines.category
        get_location = self.get_location(lines)
        count = len(get_location[0]) * 2 + 6
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
        red_mark.set_align('center')
        sheet.merge_range(1, 7, 2, 10, 'Product Stock Info', format0)
        sheet.merge_range(3, 7, 3, 10, comp, format11)
        w_house = ', '
        cat = ', '
        c = []
        d1 = d.mapped('id')
        if d1:
            for i in d1:
                c.append(self.env['product.category'].browse(i).name)
            cat = cat.join(c)
            sheet.merge_range(4, 0, 4, 1, 'Category(s) : ', format4)
            sheet.merge_range(4, 2, 4, 3 + len(d1), cat, format4)
        sheet.merge_range(5, 0, 5, 1, 'Location(s) : ', format4)
        w_house = w_house.join(get_location[0])
        sheet.merge_range(5, 2, 5, 3+len(get_location[0]), w_house, format4)
        user = self.env['res.users'].browse(self.env.uid)
        tz = pytz.timezone(user.tz)
        time = pytz.utc.localize(datetime.now()).astimezone(tz)
        sheet.merge_range('A8:G8', 'Report Date: ' + str(time.strftime("%Y-%m-%d %H:%M %p")), format1)
        sheet.merge_range(7, 7, 7, count, 'Locations', format1)
        sheet.merge_range('A9:G9', 'Product Information', format11)
        w_col_no = 6
        w_col_no1 = 7
        for i in get_location[0]:
            w_col_no = w_col_no + 2
            sheet.merge_range(8, w_col_no1, 8, w_col_no, i, format11)
            w_col_no1 = w_col_no1 + 2
        sheet.write(9, 0, 'SKU', format21)
        sheet.merge_range(9, 1, 9, 3, 'Name', format21)
        sheet.merge_range(9, 4, 9, 5, 'Category', format21)
        sheet.write(9, 6, 'Cost Price', format21)
        p_col_no1 = 7
        for i in get_location[0]:
            sheet.write(9, p_col_no1, 'Available', format21)
            sheet.write(9, p_col_no1 + 1, 'Valuation', format21)
            p_col_no1 = p_col_no1 + 2
        prod_row = 10
        prod_col = 0
        for i in get_location[1]:
            get_line = self.get_lines(d, i)
            for each in get_line:
                sheet.write(prod_row, prod_col, each['sku'], font_size_8)
                sheet.merge_range(prod_row, prod_col + 1, prod_row, prod_col + 3, each['name'], font_size_8_l)
                sheet.merge_range(prod_row, prod_col + 4, prod_row, prod_col + 5, each['category'], font_size_8_l)
                sheet.write(prod_row, prod_col + 6, each['cost_price'], font_size_8_r)
                prod_row = prod_row + 1
            break
        prod_row = 10
        prod_col = 7
        for i in get_location[1]:
            get_line = self.get_lines(d, i)
            for each in get_line:
                if each['available'] < 0:
                    sheet.write(prod_row, prod_col, each['available'], red_mark)
                else:
                    sheet.write(prod_row, prod_col, each['available'], font_size_8)
                if each['total_value'] < 0:
                    sheet.write(prod_row, prod_col + 1, each['total_value'], red_mark)
                else:
                    sheet.write(prod_row, prod_col + 1, each['total_value'], font_size_8_r)
                prod_row = prod_row + 1
            prod_row = 10
            prod_col = prod_col + 2
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
            value = available_qty * obj.standard_price
            vals = {
                'sku': obj.default_code,
                'name': obj.name,
                'category': obj.categ_id.name,
                'cost_price': obj.standard_price,
                'available': available_qty,
                'total_value': value,
            }
            lines.append(vals)
        return lines



