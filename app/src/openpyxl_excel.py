import datetime
import openpyxl


filename = r'I:\work\jiekou\c\10.xlsx'


class openpyxl_excel(object):
    def __init__(self, filename):
        inwb = openpyxl.load_workbook(filename)  # 读文件
        sheetnames = inwb.get_sheet_names()  # 获取文件所以sheet
        self.ws = inwb.get_sheet_by_name(sheetnames[0])  # 获取第一个
        self.rows = self.ws.max_row
        self.cols = self.ws.max_column
        
    def read_exel_by_cols(self, cols):  # 通过列分组获取
        if cols > self.cols:
            cols = self.cols
        rowss = self.ws.iter_cols(min_row=1, min_col=1, max_col=cols, max_row=self.rows)
        dict = dict()
        i = 1
        for row in rowss:
            list = []
            for cell in row:
                list.append(cell.value)
            dict[i] = list
            i += 1
        return dict

    def read_exel_by_rows(self, rows):  # 通过行分组获取
        if rows > self.rows:
            cols = self.rows
        rowss = self.ws.iter_rows(min_row=1, min_col=1, max_col=self.cols, max_row=rows)
        dict = dict()
        i = 1
        for row in rowss:
            list = []
            for cell in row:
                list.append(cell.value)
            dict[i] = list
            i += 1
        return dict
    
    def read_exel_all(self):  # 获取表格所以内容
        dict = dict()
        i = 1
        for eow in self.ws.values:
            p_list = []
            for values in eow:
                p_list.append(values)
            dict[i] = p_list
            i += 1
        return dict
    
    def read_by_rows_cols(self, rows, cols):
        return self.ws.cell(rows, cols).value
        
    def read_exel(self, filename):
        inwb = openpyxl.load_workbook(filename)  # 读文件
        sheetnames = inwb.get_sheet_names()  # 获取读文件中所有的sheet，通过名字的方式
        ws = inwb.get_sheet_by_name(sheetnames[0])  # 获取第一个sheet内容
        # 获取sheet的最大行数和列数
        rows = ws.max_row
        cols = ws.max_column
        for r in range(1, rows):
            for c in range(1, cols):
                print(ws.cell(r, c).value)
            if r == 10:
                break
    
    def write_excel(self):
        outwb = openpyxl.Workbook()  # 打开一个将写的文件
        outws = outwb.create_sheet(index=0)  # 在将写的文件创建sheet
        for row in range(1, 70000):
            for col in range(1, 4):
                outws.cell(row, col).value = row * 2  # 写文件
            print(row)
        saveExcel = "D:\\work\\Excel_txtProcesss\\test.xlsx"
        outwb.save(saveExcel)  # 一定要记得保存
