# coding=utf-8
# import xlrd
#
# # 打开文件
# data = xlrd.open_workbook('abc.xlsx')
# # 查看工作表
# data.sheet_names()
# print("sheets：" + str(data.sheet_names()))
#
# # 通过文件名获得工作表,获取工作表1
# table = data.sheet_by_name('工作表1')
#
# # 打印data.sheet_names()可发现，返回的值为一个列表，通过对列表索引操作获得工作表1
# # table = data.sheet_by_index(0)
#
# # 获取行数和列数
# # 行数：table.nrows
# # 列数：table.ncols
# print("总行数：" + str(table.nrows))
# print("总列数：" + str(table.ncols))
#
# # 获取整行的值 和整列的值，返回的结果为数组
# # 整行值：table.row_values(start,end)
# # 整列值：table.col_values(start,end)
# # 参数 start 为从第几个开始打印，
# # end为打印到那个位置结束，默认为none
# for i in range(1, table.nrows):
#     print("整行值：" + str(table.row_values(i)))
# for n in range(0, table.ncols):
#     print("整列值：" + str(table.col_values(n)))
# print(table.row_values(3)[1])
# # 获取某个单元格的值，例如获取B3单元格值
# cel_B3 = table.cell(3, 2).value
# print("第三行第二列的值：" + cel_B3)

alist = ((1, '品园1楼'), (11, '品园2楼'), (18, '品园3楼'), (29, '品园4楼'), (40, '品园5楼'), (51, '品园6楼'), (63, '知行1楼'), (78, '知行2楼'),(95, '知行3楼'), (111, '知行4楼'), (120, '知行5楼'), (133, '宜园3楼'), (150, '红1楼'), (154, '红2楼'), (158, '红3楼'), (162, '北园2楼'),(167, '北园5楼'), (173, '北园6楼'), (177, '东风6楼'), (184, '东风7楼'), (191, '培训1楼'))

# with open('config1.txt', 'w', encoding='utf-8') as f:
#     f.write(str(alist))
#     f.close()

# with open('config1.txt', 'r', encoding='utf-8') as f:
#     aa = f.readlines()
#     print(aa)
#     a_list = aa[0].split('---')
#     print(a_list)
#     for i in a_list:
#         print(i.split('.'))

# print(alist, type(alist))
# print(list(alist), type(list(alist)))
# res_list = []
# for i in alist:
#     if len(i) == 1:
#         res_list.append(i[0])
#     else:
#         res_list.append(list(i))
# print(res_list, type(res_list))

p_list = ['失联.txt', '未归.txt', '晚归.txt', '正常.txt']
for p in p_list:
    print(p[:2])
    
from datetime import datetime
from datetime import timedelta
talk_time = '2020-08-05 18:30:00'
last_time = '2020-08-05 18:00:00'
lo_time = datetime.strptime(talk_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
in_time = int(timedelta.total_seconds(lo_time)/60)
print(in_time, type(in_time))
# datetime.timetz(lo_time)
# if lo_time > datetime.strptime('0:15:00', '%H:%M:%S'):
#     print(111)
# print(datetime.strptime(lo_time, '%H:%M:%S'))
print(lo_time)
