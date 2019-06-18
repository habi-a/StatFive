#-*- coding: utf-8 -*-
from  xlsxwriter import Workbook

from datetime import datetime

import os


class Excel():

    def __init__(self, file, manager= ''):
        self.file = Workbook(file)

    def close(self):
        self.file.close()

    def add_score_card(self,l=[]):
        d_sc = {e['date']:e for e in l}
        key = sorted([key for key in d_sc],reverse=True)[0]
        worksheet = self.file.add_worksheet('Score Card')
        worksheet.write('A1', '%s Score Card (%s)'%(d_sc[key]['origin'],
                                                    datetime.strptime(key,'%Y%m%d').strftime('%Y/%m/%d'))
                        )
        worksheet.write('A3','Nb risk')
        worksheet.write('B3',d_sc[key]["total_risk"])
        worksheet.write('A4','Nb user')
        worksheet.write('B4',d_sc[key]["total_user"])
        worksheet.write('A5','Nb risked user')
        worksheet.write('B5',d_sc[key]["user_with_conflict"])
        worksheet.write('A7','% risked user')
        worksheet.write_formula('B7',
                                '=B5/B4*100' if d_sc[key]["total_user"] != 0 else 0 )
        worksheet.write('A8','risk per user')
        worksheet.write_formula('B8',
                                '=B3/B5' if d_sc[key]["user_with_conflict"] != 0 else 0)
        
        header = ['']
        header.extend(['risk %s'%(int(risk)*'*')
                       for risk in sorted([risk for risk in d_sc[key] if len(risk)==1])])
        values = [header]
        for key in sorted([key for key in d_sc]):
            li = []
            li.append(datetime.strptime(key,'%Y%m%d').strftime('%Y/%m/%d'))
            for risk in sorted([risk for risk in d_sc[key] if len(risk)==1]):
                li.append(d_sc[key][risk])
            values.append(li)
        col = 3
        row = 2
        for x in range(len(values)):
            for y in range(len(values[x])):
                worksheet.write(row+y,col+x,values[x][y])
        
        series = [row,col,col+len(values)-1,row+len(values[0])-1]
        self.radar(worksheet,len(values),series,'D10')
        self.line(worksheet,series)
  
        

    def radar(self,ws,nb_sc,series,position):
        # radar chart
        radar = self.file.add_chart({'type': 'radar'})
        # adding the serie
        for x in range(1,nb_sc,1):
            radar.add_series({'name':['Score Card',
                                      series[0],
                                      series[1]+x],
                              'categories': ['Score Card',
                                             series[0]+1,
                                             series[1],
                                             series[3],
                                             series[1]],
                              'values':['Score Card',
                                        series[0]+1,
                                        series[1]+x,
                                        series[3],
                                        series[1]+x],
                              'line': {'width': 1}})
        radar.set_title ({'name':'Score Card'}
                          )
        radar.set_y_axis({'log_base':10,
                          'major_gridlines': {'visible': False},
                          })
        # adding the chart in the page
        ws.insert_chart('D10', radar,
                               )

    def line(self,ws,series):
        position = {7:'A25',
                    6:'I25',
                    5:'A40',
                    4:'I40',
                    3:'A55',
                    }
        for x in range(series[0]+1,series[3]+1,1):
            line = self.file.add_chart({'type': 'line'})
            line.set_title({'name': ['Score Card',x,3]})
            line.add_series({'categories': ['Score Card', series[0], series[1]+1, series[0], series[-2]],
                             'values': ['Score Card', x, series[1]+1, x,series[-2]],
                             'name':['Score Card',x,3],
                             'trendline': {'type': 'linear',
                                           'name': 'trendline'},}
                            )
            ws.insert_chart(position[x], line)
            
    def add_content(self,worksheet_name,header,ll_content):
        worksheet = self.file.add_worksheet(worksheet_name)
        worksheet.write_row('A1', header)
        worksheet.add_table(0,
                            0,
                            len(ll_content),
                            len(header)-1,
                            {'data': ll_content,
                             'columns' : [{'header':e}
                                          for e in header]
                             }
                            )


