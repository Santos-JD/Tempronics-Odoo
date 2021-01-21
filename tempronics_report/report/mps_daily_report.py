from odoo import models
from datetime import datetime, timedelta
from odoo.tools.translate import _
import pytz
from odoo.exceptions import UserError
import string

class MpsDaily(models.AbstractModel):
    _name = 'report.tempronics_report.mps_daily'
    _inherit = 'report.report_xlsx.abstract'

    def GetColExcel(self,Col):
        Abc = list(string.ascii_uppercase)
        LenAbc = len(Abc)
        if Col >= LenAbc:
            x = int((Col / LenAbc) - 1)
            y = Col % LenAbc
            letra = Abc[x] + Abc[y] #Llega a romperse en la secuencia ZZ -> AAA Numpero maximo de columnas 702
        else: 
            letra = Abc[Col]
        return letra


    def rangeDate(self,date_from,date_to,week_days,col):
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        days_between = date_to - date_from
        TitlesDates = []
        Dates = {}
        Data = {}
        for i in range(days_between.days+1):
            new_day = date_from + timedelta(days=i)
            iso = new_day.isocalendar()
            week = iso[1]
            weekday = iso[2]
            if weekday <= week_days:
                strdate =  str(new_day.month) +"/"+ str(new_day.day)
                TitlesDates.append(strdate)
                Dates[str(new_day.date())] = col
                col += 1
            else:
                Dates[str(new_day.date())] = col
        
        Data['Dates'] = Dates
        Data['TitlesDates'] = TitlesDates
        return Data

    def CreateDic(self,objOrders):
        OrderData = {}

        for order in objOrders:
            DateAux = {}
            Product = {}
            strDate = str(order.commitment_date.date())
            if order.order_id.name in OrderData:
                Product = OrderData[order.order_id.name]
                if order.product_id.id in Product: #Verificamos si existe ya el producto en product
                    DateAux = Product[order.product_id.id]['Date'] #obtenemos las fechas del producto
                    if strDate in DateAux:
                        #Ya existe la fecha en el producto actual
                        #obtenemos la cantidad que tenga y la sumamos
                        DateAux[strDate] += order.product_uom_qty
                    else:
                        #Si no existe la creamos con su cantidad actual
                        DateAux[strDate] = order.product_uom_qty

                    Product[order.product_id.id]['Date'] = DateAux
                else:
                    DateAux[strDate] = order.product_uom_qty
                    Product[order.product_id.id] = {'product':order.product_id.default_code,'Date': DateAux, 'Obj': order}
            else:
                DateAux[strDate] = order.product_uom_qty
                Product[order.product_id.id] = {'product':order.product_id.default_code,'Date': DateAux, 'Obj': order}
                
            OrderData[order.order_id.name] = Product
        
        return OrderData

    def generate_xlsx_report(self, workbook, data, objects):
        form = data['form']
        idsSale = data['sale_orders']
        saleOrders = self.env['sale.order.line'].browse(idsSale)
        document_name = form['document_name']
        date_from = form['date_from']
        date_to = form['date_to']
        sheet_title = ['No.','Part No.','Description','SO #','Qty']
        DataDates = self.rangeDate(date_from,date_to,5,len(sheet_title)+1)
        arrDate = DataDates['TitlesDates']
        ColDates = DataDates['Dates']
        sheet_title = sheet_title + arrDate
        row = 6
        sheet = workbook.add_worksheet(_('MPS'))

        title_style = workbook.add_format({ 
                                            'bold': True,
                                            'bottom': 1,
                                            'align': 'left',
                                            'font_size': 14
                                         })

        title_table_style = workbook.add_format({
                                                    'bold': True,
                                                    'align': 'center',
                                                    'font_size': 12    
                                                })

        title_table_date_format_style = workbook.add_format({
                                                    'bold': True,
                                                    'align': 'center',
                                                    'font_size': 12    
                                                })
                                                

        info_table_style = workbook.add_format({
                                                    'border': 1,
                                                    'font_size': 11    
                                                })

        info_table_center_style = workbook.add_format({
                                                    'border': 1,
                                                    'align': 'center',
                                                    'font_size': 11 
                                                })

        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 6)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 40)
        sheet.set_column(4, 4, 8)
        sheet.set_column(5, 5, 8)
        sheet.set_zoom(80)
        sheet.freeze_panes(6,6)


        user = self.env['res.users'].browse(self.env.uid)
        tz = pytz.timezone(user.tz)
        time = pytz.utc.localize(datetime.now()).astimezone(tz)

        sheet.write(1,1,document_name,title_style)
        sheet.write(2,1,'Report Date: '+ str(time.strftime("%Y-%m-%d %H:%M %p")),title_style)

        
        sheet.write_row(5, 1, sheet_title, title_table_style)
        #sheet.write_row(5,len(sheet_title)+1,arrDate,title_table_date_format_style)
        
        DataOrders = self.CreateDic(saleOrders)
        
        MaxCol = self.GetColExcel(len(sheet_title))

        for okey,order in DataOrders.items():
            for lkey,line in order.items():
                sheet.write(row,1,row-5,info_table_center_style)
                sheet.write(row,2,line['product'],info_table_center_style)
                sheet.write(row,3,line['Obj'].product_id.name,info_table_style)
                sheet.write(row,4,okey,info_table_center_style)
                #sheet.write(row,5,0.0,info_table_center_style)
                strSuma = '=SUM(G'+str(row+1)+':'+MaxCol+str(row+1)+')'
                sheet.write_formula(row,5,strSuma,info_table_center_style)
                #com_date = str(line['Obj'].commitment_date.date())
                for fecha in line['Date']:
                    sheet.write(row,ColDates[fecha],line['Date'][fecha],info_table_center_style)
                row += 1

        
