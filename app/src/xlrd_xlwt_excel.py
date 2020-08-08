import xlwt
import xlrd
import threading
import os


class xlrd_xlwt_excel(object):  # xlrd xlwt 处理csv文件
    _instance_lock = threading.Lock()
    
    def __init__(self, filename=None, index=0):
        if os.path.exists(filename):
            self.inwb = xlrd.open_workbook(filename)  # 读文件
            self.sheetnames = self.inwb.sheet_names()  # 获取文件所以sheet
            self.ws = self.inwb.sheet_by_name(self.sheetnames[index])  # 默认获取第一个
            self.rows = self.ws.nrows
            self.cols = self.ws.ncols
            self.filename = filename
    
    def __new__(cls, *args, **kwargs):  # 单例
        if not hasattr(xlrd_xlwt_excel, "_instance"):
            with xlrd_xlwt_excel._instance_lock:
                if not hasattr(xlrd_xlwt_excel, "_instance"):
                    xlrd_xlwt_excel._instance = object.__new__(cls)
        return xlrd_xlwt_excel._instance

    def read_execl_by_cols(self, cols=0):  # 通过列分组获取
        """ clos 列号 从零开始 """
        if not self.inwb:
            return "初始化失败或文件不存在"
        if cols > self.cols:
            cols = self.cols
        dict_cols = dict()
        i = 0
        for c in range(cols):
            list = []
            cols = self.ws.col(c)
            for cell in cols:
                list.append(cell.value)
            dict_cols[i] = list.copy()
            i += 1
        return dict_cols

    def read_execl_by_rows(self, rows=0):  # 通过行分组获取
        """ clos 行号 从零开始 """
        if not self.inwb:
            return "初始化失败或文件不存在"
        if rows > self.rows:
            rows = self.rows
        dict_rows = dict()
        i = 0
        for r in range(rows):
            list = []
            row = self.ws.row(r)
            for cell in row:
                list.append(cell.value)
            dict_rows[i] = list.copy()
            i += 1
        return dict_rows

    def read_execl_all(self):  # 获取表格所以内容
        """ 获取表格所有内容 """
        if not self.ws:
            return "初始化失败或文件不存在"
        dict_all = dict()
        i = 0
        for e in range(self.rows):
            p_list = []
            eow = self.ws.row(e)
            for values in eow:
                p_list.append(values.value)
            dict_all[i] = p_list.copy()
            i += 1
        return dict_all

    def read_by_rows_cols(self, rows, cols):
        """ 获取表格指定的单元格 """
        if not self.ws:
            return "初始化失败或文件不存在"
        return self.ws.cell(rows, cols).value

    @classmethod
    def write_new_file_excel(cls, savefilename=None, datadict=None):
        """写表格，datadict以每行存list或元组，总的以字典格式传递
        :param savefilename : 文件路径及名字
        :type savefilename : str
        :param datadict : 数据字典
        :type datadict : dict
        """
        if not datadict:
            return "空数据"
        try:
            # style = xlwt.XFStyle()  # 初始化样式
            outwb = xlwt.Workbook()  # 打开一个将写的文件
            outws = outwb.add_sheet('sheet1')  # 在将写的文件创建sheet
        except Exception as e:
            print("Excel新建表：", e)
            return "处理新建表格失败"
        rows = 0
        for row in datadict:
            cols = 0
            datalist = datadict[row]
            for col in datalist:
                outws.cell(rows, cols).value = col  # 写文件
                cols += 1
            rows += 1
        try:
            if not savefilename:
                return "文件路径不存在"
            outwb.save(savefilename)  # 一定要记得保存
        except Exception as e:
            print("Excel保存：", e)
            return "文件保存失败"
        return "OK"
    
    
if __name__ == '__main__':
    a = xlrd_xlwt_excel(r'I:\work\jiekou\c\user10.csv')
    # print(a.read_by_rows_cols(0, 0))
    # print(a.read_execl_by_cols(15))
    # print(a.read_execl_all())
    print(a.read_execl_by_rows(10000))

