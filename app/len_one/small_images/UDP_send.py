import socket, time


def main():
    # 创建一个udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 可以使用套接字收发数据
    # udp_socket.sendto(内容（必须是bytes类型）, 对方的ip以及port)
    # udp_socket.sendto(b'hahaha', ('192.168.1.103', 8001))
    a = """文章千古事，得失寸心知。作者皆殊列，名声岂浪垂。
骚人嗟不见，汉道盛于斯。前辈飞腾入，馀波绮丽为。
后贤兼旧列，历代各清规。法自儒家有，心从弱岁疲。
永怀江左逸，多病邺中奇。騄骥皆良马，骐驎带好儿。
车轮徒已斫，堂构惜仍亏。漫作潜夫论，虚传幼妇碑。
缘情慰漂荡，抱疾屡迁移。经济惭长策，飞栖假一枝。"""
    sum = 0
    while sum <= 10000:
        # 从键盘获取数据(第二种方法)
        # send_data = input('请输入要发送的内容：')
        send_data = a + str(sum)
        # 如果输入的数据是exit,那么就退出程序
        # if send_data == 'exit':
        #     break
        udp_socket.sendto(send_data.encode('utf-8'), ('47.113.103.32', 8055))
        sum += 1
        time.sleep(0.1)
    
    print('----22------', sum)
    print(send_data)
    # 关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    main()
