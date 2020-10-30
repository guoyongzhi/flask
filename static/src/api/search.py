import requests

from bs4 import BeautifulSoup


def get_html(url, headers):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text


def get_pages(html, count):
    soup = BeautifulSoup(html, 'html.parser')
    all_topics = soup.find_all('tr')[1:]
    if count <= 0:
        return
    if count > 30:
        count = 30
    top10 = ''
    for each_topic in all_topics:
        topic_times = each_topic.find('td', class_='last')  # 搜索指数
        topic_rank = each_topic.find('td', class_='first')  # 排名
        topic_name = each_topic.find('td', class_='keyword')  # 标题目
        
        if topic_rank != None and topic_name != None and topic_times != None:
            topic_rank = each_topic.find('td', class_='first').get_text().replace(' ', '').replace('\n', '')
            topic_name = each_topic.find('td', class_='keyword').get_text().replace(' ', '').replace('\n', '')
            topic_times = each_topic.find('td', class_='last').get_text().replace(' ', '').replace('\n', '')
            # print('排名：{}，标题：{}，热度：{}'.format(topic_rank,topic_name,topic_times))
            tplt = "排名：{0:^4}\t标题：{1:{3}^15}\t热度：{2:^8}"
            # print(tplt.format(topic_rank, topic_name, topic_times, chr(12288)))
            if int(topic_rank) <= count:
                top10 += str(topic_rank) + '、' + topic_name[:-6] + '\n'
    return top10


def main(count=10):
    # 百度热点排行榜单链接
    url = 'http://top.baidu.com/buzz?b=1&fr=20811'
    headers = {'User-Agent': 'Mozilla/5.0'}
    html = get_html(url, headers)
    return get_pages(html, count)


if __name__ == '__main__':
    # print(main())
    """ 处理本地数据未同步至redis（已经执行）
    import json
    from axf.dbredis import db_redis
    with open('config.txt', 'r', encoding='utf-8') as file:
        a_list = []
        aa = file.readlines()
        for a in aa:
            a_list.append(a[:-4])
        file.close()
        game_dict = json.loads(a_list[2])
    users_keys_list = db_redis(14).r.keys()
    del_list = []
    # print(game_dict)
    for g in game_dict.keys():
        if str('19_') + g in users_keys_list:
            del_list.append(g)
            res = db_redis(14).get_owner(str('19_') + g)
            new = game_dict[g]
            result = json.loads(res)
            result['point'] += new[1]
            result['gold'] += new[2]
            print(res, game_dict[g])
            print(result)
            re = db_redis(14).set_value(name=str('19_') + g, value=json.dumps(result))
    for i in del_list:
        del game_dict[i]
    print(game_dict.keys())
    qun_list = user_list = user_idiom_list = red_packet_list = idiom_list = ana_list = users_list = sign_in_list = []
    this_num = 0
    idiom_dict = dict()
    with open('config.txt', 'w', encoding='utf-8') as file:
        file.write('.'.join(qun_list))
        file.write('---\n')
        file.write('.'.join(user_list))
        file.write('---\n')
        file.write(json.dumps(game_dict))
        file.write('---\n')
        file.write('.'.join(user_idiom_list))
        file.write('---\n')
        file.write('.'.join(red_packet_list))
        file.write('---\n')
        file.write('.'.join(idiom_list))
        file.write('---\n')
        file.write(str(this_num))
        file.write('---\n')
        file.write('.'.join(ana_list))
        file.write('---\n')
        file.write('.'.join(sign_in_list))
        file.write('---\n')
        file.write(json.dumps(idiom_dict))
        file.write('---\n')
        file.write('.'.join(users_list))
        file.write('---\n')
        file.close()
    """
    """
    import json
    from axf.dbredis import db_redis
    # qun_id = 19
    # result = db_redis(13).get_owner(owner=str(qun_id))
    # print(result)
    # if result:
    #     sign_list = result[1:-1].replace("'", '').split(',')
    #     sign_in_list = sign_list
    # if sign_in_list:
    #     info = '今日当前签到排行榜\n'
    #     sign_in_list_len = 1
    #     for i in sign_in_list:
    #         if len(sign_in_list) == sign_in_list_len:
    #             info += '第' + str(sign_in_list_len) + '名：' + i
    #         else:
    #             info += '第' + str(sign_in_list_len) + '名：' + i + '\n'
    #         sign_in_list_len += 1
    # else:
    #     info = '当前签到排行榜\n无人签到'
    #
    # print(info)
    qun_id = 1
    sign_in_list = []
    a = ['珠峰', '🍦🍦🍦', 'Jung(小华)', '"Jadore"', 'Song❤🚴🏸🚶', 'A小燕', '槑俐👣  \\\\\\\\U0001f929', '过客', 'LIU ', '成成']
    for ai in a:
        result = db_redis(13).get_owner(owner=str(qun_id))
        # print(result)
        if result:
            sign_list = result[1:-1].replace("'", '').split(',')
            print(sign_list)
            sign_in_list = sign_list
        sign_in_list.append(ai)
        db_redis(13).r.rpush(str(qun_id), *tuple(sign_in_list))
        sign_in_list.clear()
        input()
    """

