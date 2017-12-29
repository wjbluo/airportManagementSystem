# -*- coding: utf-8 -*-
'''
xlrd读取excel数据 转化为dic

'''
import  xdrlib ,sys
import json
import xlrd
from datetime import date,datetime

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引 readfirst:是否需要提取第一行数据
def excel_table_byindex(data,colnameindex=0,by_index=0,readfirst=0):

    table = data.sheets()[by_index]

    nrows = table.nrows #行数
    ncols = table.ncols #列数
    for row in range(0, nrows):   # 顺序搜索excel 如发现时间格式，先把其转化为String
        for col in range(0, ncols):
            if (table.cell(row, col).ctype == 3):
                date_value = xlrd.xldate_as_tuple(table.cell_value(row, col), data.datemode)
                date_tmp = date(*date_value[:3]).strftime('%Y-%m-%d')
                table.put_cell(row, col,1,date_tmp,0)


    colnames =  table.row_values(colnameindex) # 读取 首行作为 dict的键
    # print json.dumps(colnames, encoding="UTF-8", ensure_ascii=False) # 将dic内容中文输出
    firstcol = table.row_values(readfirst)
    list =[]
    for rownum in range(colnameindex+1,nrows):

         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list,firstcol

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
# def excel_table_byname(file= 'E:\\django.xlsx',colnameindex=0,by_name=u'Sheet1'):
#     data = open_excel(file)
#     table = data.sheet_by_name(by_name)
#     nrows = table.nrows #行数
#     colnames =  table.row_values(colnameindex) #某一行数据
#     list =[]
#     for rownum in range(1,nrows):
#          row = table.row_values(rownum)
#          if row:
#              app = {}
#              for i in range(len(colnames)):
#                 app[colnames[i]] = row[i]
#              list.append(app)
#     return list

# def main():
#     pass
    # tables = excel_table_byindex('E:\\django.xlsx')
    # for row in tables:
    #     print (json.dumps(row, encoding="UTF-8", ensure_ascii=False))

    # tables = excel_table_byname()
    # for row in tables:
    #     print row

# if __name__=="__main__":
#     main()