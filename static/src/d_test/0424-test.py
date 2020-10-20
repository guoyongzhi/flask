# from urllib.request import urlopen, Request
# from urllib.error import URLError
# from urllib.parse import urlencode
# import json
#
#
# class TuringChatMode(object):
#     """this mode base on turing robot"""
#
#     def __init__(self):
#         # API接口地址
#         self.turing_url = 'http://www.tuling123.com/openapi/api?'
#
#     def get_turing_text(self, text):
#         ''' 请求方式:   HTTP POST
#             请求参数:   参数      是否必须        长度          说明
#                         key        必须          32           APIkey
#                         info       必须          1-32         请求内容，编码方式为"utf-8"
#                         userid     必须          32           MAC地址或ID
#         '''
#         turing_url_data = dict(key='fcbf9efe277e493993e889eabca5b331', info=text, userid='60-14-B3-BA-E1-4D',
#
#         )
#         # print("The things to Request is:",self.turing_url + urlencode(turing_url_data))
#         self.request = Request(self.turing_url + urlencode(turing_url_data))
#         # print("The result of Request is:",self.request)
#
#         try:
#             w_data = urlopen(
#                 self.request)  # print("Type of the data from urlopen:",type(w_data))  # print("The data from urlopen is:",w_data)
#         except URLError:
#             raise IndexError("No internet connection available to transfer txt data")  # 如果发生网络错误，断言提示没有可用的网络连接来传输文本信息
#         except:
#             raise KeyError("Server wouldn't respond (invalid key or quota has been maxed out)")  # 其他情况断言提示服务相应次数已经达到上限
#
#         response_text = w_data.read().decode('utf-8')
#         # print("Type of the response_text :",type(response_text))
#         # print("response_text :",response_text)
#
#         json_result = json.loads(response_text)
#         # print("Type of the json_result :",type(json_result))
#         return json_result['text']
#
#
# if __name__ == '__main__':
#     print("Now u can type in something & input q to quit")
#
#     turing = TuringChatMode()
#
#     while True:
#         msg = input("\nMaster:")
#         if msg == 'q':
#             exit("u r quit the chat !")  # 设定输入q，退出聊天。
#         else:
#             turing_data = turing.get_turing_text(msg)
#             print("Robot:", turing_data)

# import requests, datetime
#
# if __name__ == "__main__":
#     talk = input("请输入第一句消息开启对话：")
#     while True:
#         res = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
#         res = res.json()
#         print("小云：{}  ({})".format(res["content"], datetime.datetime.now()))
#         if res["content"] == '%菲菲%':
#             re = res["content"].split('菲菲')[0]
#             ree = res["content"].split('菲菲')[1]
#             print(re + '小志' + ree)
#         talk = input("回复：")


# import random
#
# current_word = start_data[random.randint(0, len(start_data) - 1)]
import struct
import os

# 搜狗的scel词库就是保存的文本的unicode编码，每两个字节一个字符（中文汉字或者英文字母）
# 找出其每部分的偏移位置即可
# 主要两部分
# 1.全局拼音表，貌似是所有的拼音组合，字典序
#       格式为(index,len,pinyin)的列表
#       index: 两个字节的整数 代表这个拼音的索引
#       len: 两个字节的整数 拼音的字节长度
#       pinyin: 当前的拼音，每个字符两个字节，总长len
#
# 2.汉语词组表
#       格式为(same,py_table_len,py_table,{word_len,word,ext_len,ext})的一个列表
#       same: 两个字节 整数 同音词数量
#       py_table_len:  两个字节 整数
#       py_table: 整数列表，每个整数两个字节,每个整数代表一个拼音的索引
#
#       word_len:两个字节 整数 代表中文词组字节数长度
#       word: 中文词组,每个中文汉字两个字节，总长度word_len
#       ext_len: 两个字节 整数 代表扩展信息的长度，好像都是10
#       ext: 扩展信息 前两个字节是一个整数(不知道是不是词频) 后八个字节全是0
#
#      {word_len,word,ext_len,ext} 一共重复same次 同音词 相同拼音表


# 拼音表偏移，
startPy = 0x1540;

# 汉语词组表偏移
startChinese = 0x2628;

# 全局拼音表
GPy_Table = {}

# 解析结果
# 元组(词频,拼音,中文词组)的列表
GTable = []


# 原始字节码转为字符串
def byte2str(data):
    pos = 0
    str = ''
    while pos < len(data):
        c = chr(struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0])
        if c != chr(0):
            str += c
        pos += 2
    return str


# 获取拼音表
def getPyTable(data):
    data = data[4:]
    pos = 0
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        pos += 2
        lenPy = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        pos += 2
        py = byte2str(data[pos:pos + lenPy])
        
        GPy_Table[index] = py
        pos += lenPy


# 获取一个词组的拼音
def getWordPy(data):
    pos = 0
    ret = ''
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        ret += GPy_Table[index]
        pos += 2
    return ret


# 读取中文表
def getChinese(data):
    pos = 0
    while pos < len(data):
        # 同音词数量
        same = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        
        # 拼音索引表长度
        pos += 2
        py_table_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        
        # 拼音索引表
        pos += 2
        py = getWordPy(data[pos: pos + py_table_len])
        
        # 中文词组
        pos += py_table_len
        for i in range(same):
            # 中文词组长度
            c_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 中文词组
            pos += 2
            word = byte2str(data[pos: pos + c_len])
            # 扩展数据长度
            pos += c_len
            ext_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 词频
            pos += 2
            count = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            
            # 保存
            GTable.append((count, py, word))
            
            # 到下个词的偏移位置
            pos += ext_len


def scel2txt(file_name):
    print('-' * 60)
    with open(file_name, 'rb') as f:
        data = f.read()
    
    print("词库名：", byte2str(data[0x130:0x338]))  # .encode('GB18030')
    print("词库类型：", byte2str(data[0x338:0x540]))
    print("描述信息：", byte2str(data[0x540:0xd40]))
    print("词库示例：", byte2str(data[0xd40:startPy]))
    
    getPyTable(data[startPy:startChinese])
    getChinese(data[startChinese:])


if __name__ == '__main__':
    
    # scel所在文件夹路径
    in_path = "I:/work/flask/static/src/api"
    # 输出词典所在文件夹路径
    out_path = "coal_dict.txt"
    
    fin = [fname for fname in os.listdir(in_path) if fname[-5:] == ".scel"]
    for f in fin:
        f = os.path.join(in_path, f)
        scel2txt(f)

    # 保存结果
    with open(out_path, 'w', encoding='utf8') as f:
        f.writelines([word + '\n' for count, py, word in GTable])

    # file = open(out_path, encoding='utf-8').readlines()
    # f = open('zidian.txt', 'w')
    # x = {}
    # num = 0
    # for i in file:
    #     print
    #     i[2:10]
    #     x[num] = i[2:10]
    #     f.write("'%s':u'%s',\n" % (num, i[2:10]))
    #     num += 1
    # f.close()
    #
