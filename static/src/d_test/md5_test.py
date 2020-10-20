import hashlib
import datetime


# import sys
def Findmd5(args):
    md = args.hashvalue
    starttime = datetime.datetime.now()
    for i in open(args.file):
        md5 = hashlib.md5()  # 获取一个md5加密算法对象
        rs = i.strip()  # 去掉行尾的换行符
        md5.update(rs.encode('utf-8'))  # 指定需要加密的字符串
        newmd5 = md5.hexdigest()  # 获取加密后的16进制字符串
        # print newmd5
        if newmd5 == md:
            print
            '明文是：' + rs  # 打印出明文字符串
            break
        else:
            pass
    
    endtime = datetime.datetime.now()
    print
    endtime - starttime  # 计算用时，非必须


if __name__ == '__main__':
    import argparse  # 命令行参数获取模块
    
    parser = argparse.ArgumentParser(usage='Usage:./findmd5.py -l 密码文件路径 -i 哈希值 ',
                                     description='help info.')  # 创建一个新的解析对象
    parser.add_argument("-l", default='wordlist.txt', help="密码文件.", dest="file")  # 向该对象中添加使用到的命令行选项和参数
    parser.add_argument("-i", dest="hashvalue", help="要解密的哈希值.")
    
    args = parser.parse_args()  # 解析命令行
    Findmd5(args)
