#*_*coding:utf-8*_*
import xlrd as excel
import gc #垃圾回收
import os
from aceui.lib import gl
from xlutils.copy import copy




#Excel操作
class Excel(object):
    __slots__ = ['excelPath']

    def __init__(self,excelPath):
        self.excelPath =excelPath

    #创建workbook对象
    def OpenExcel(self,file='file.xls'):
        try:
            ret = excel.open_workbook(filename=self.excelPath)
            #data = excel.open_workbook(filename=self.excelPath)
            return  ret
        except Exception as ex:
            print(str(ex))

    #获取指定行数据,返回数组
    def getRowData(self,rownum =0):
        try:
            data = self.OpenExcel(self.excelPath)
            table = data.sheet_by_index(0)
        except Exception as ex:
            return ex.message()
        return table.row_values(rownum)


    def getCardNo(self,start_col=0,cell_col=1,cell_valueType=0,sheet_name='Sheet1'):
        """
        获取实体卡，卡号
        :param start_col: 定义列所在行号
        :param sheet_name: Sheet名称
        :return: 卡号或None
        """
        cardNo = None
        data = self.OpenExcel(self.excelPath)
        table = data.sheet_by_name(sheet_name)
        rowCount = table.nrows

        for n in range(1,rowCount):
            openCardflag = table.cell(n,2).value
            if str(openCardflag).upper() != 'Y':
                cardNo = str(table.cell(n,cell_col).value) #卡号
                newData = copy(data)
                ws = newData.get_sheet(0)
                ws.write(n,2,'Y')
                newData.save(self.excelPath)
                break

        if cell_valueType ==0:
            cardNo = cardNo[1:]

        return cardNo




    #根据sheet名获取所有行数据，数组返回
    def getExcelDataByName(self,start_col=4,sheet_name='Sheet1'):

        data = self.OpenExcel(self.excelPath)
        table = data.sheet_by_name(sheet_name)
        RowCount = table.nrows
        ColCount = table.ncols
        ColName = table.row_values(start_col) #获取行，列名行数据，返回数组
        #print ColName
        list=[] #存储行数据，内容字典对象
        #遍历，列名与行数据存储在字典中，并将字典对象存在list中

        for rowNum in range(start_col+1,RowCount):
            #row = table.row_values(rowNum)
            dict = {}

            if table.cell_value(rowNum,0) !='END':
                #print type(table.cell_value(rowNum, 0))
                for i in range(len(ColName)):
                    dict[ColName[i]]=table.cell_value(rowNum,i)
                list.append(dict)
            else:
                break
        gc.collect()
        return list





if __name__=="__main__":
    excelPath = os.path.join(gl.dataPath, 'posChargeCard.xls').decode('utf-8')
    a =  Excel(excelPath).getCardNo(cell_col=0,cell_valueType=1)
    print(int(float(a)))