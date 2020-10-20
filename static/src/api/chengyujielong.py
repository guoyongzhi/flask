from IPython.core.interactiveshell import InteractiveShell
from pypinyin import pinyin, lazy_pinyin, Style
import random

InteractiveShell.ast_node_interactivity = "all"

idiom_dic = {}
idiom_list = []
idiom_char_dic = {}

with open('coal_dict.txt', 'r', encoding='utf8') as r:
    for line in r:
        line = line.strip()
        if line is None or line == '':
            continue
        idiom_list.append(line)
        key = lazy_pinyin(line)[0]
        value = ''
        if key in idiom_dic.keys():
            value = idiom_dic[key] + ',' + line
        else:
            value = line
        idiom_dic[key] = value
        # 汉字接龙
        key_char = line[0]
        value_char = ''
        if key_char in idiom_char_dic.keys():
            value_char = idiom_char_dic[key_char] + ',' + line
        else:
            value_char = line
        idiom_char_dic[key_char] = value_char


# 汉字接龙，polyphone -- 是否匹配读音
def idiom_next_char(idiom, polyphone=False):
    if idiom not in idiom_list:
        res = idiom + ' 这不是个成语哦'
    else:
        last = idiom[len(idiom) - 1]
        if polyphone:
            if last not in idiom_char_dic:
                res = idiom + ' 这不是个成语哦'
            else:
                aa = idiom_char_dic[last]
                last = lazy_pinyin(idiom)[len(idiom) - 1]
                bb = idiom_dic[last]
                aa_list = aa.split(',')
                bb_list = bb.split(',')
                cd_list = set(aa_list).intersection(set(bb_list))  # 求并集
                res = cd_list
        else:
            if last not in idiom_char_dic:
                res = idiom + ' 这不是个成语哦'
            else:
                res = idiom_char_dic[last]
                res = res.split(',')
    return res


# 拼音接龙
def idiom_next(idiom):
    if idiom not in idiom_list:
        res = idiom + ' is not one idiom'
    else:
        last = lazy_pinyin(idiom)[len(idiom) - 1]
        if last not in idiom_dic:
            res = 'library without the supply idioms'
        else:
            res = idiom_dic[last]
    return res


# print(idiom_next('怒发冲冠'))

# 汉字定长接龙
def idiom_multi_char_length(idiom, length=10, polyphone=False):
    index = 0
    res_list = [idiom]
    while index < length:
        res = idiom_next_char(idiom, polyphone)
        if 'idiom' in res:
            break
        else:
            res_next = res.split(',')
            idiom = res_next[0]
        res_list.append(idiom)
        index = index + 1
    return res_list


# 拼音定长接龙
def idiom_multi_length(idiom, length=10):
    index = 0
    res_list = [idiom]
    while index < length:
        res = idiom_next(idiom)
        if 'idiom' in res:
            break
        else:
            res_next = res.split(',')
            idiom = res_next[0]
        res_list.append(idiom)
        index = index + 1
    return res_list


def check_none_follow_list():
    none_follow = []
    for idiom in idiom_list:
        res = idiom_next_char(idiom, polyphone=True)
        if 'idiom' in res:
            none_follow.append(idiom)
    return none_follow


users_list = []
nn = ''
idiom_dict = dict()


def chengyujielong(s='', name=''):
    global nn, users_list, idiom_dict
    if s == '':
        users_list = []
        current_word = idiom_list[random.randint(0, len(idiom_list) - 1)]
        nn = current_word
        users_list.append(current_word)
        idiom_dict[name] = nn, users_list
        return current_word
    try:
        if name in idiom_dict:
            new = idiom_dict[name]
            nn = new[0]
            users_list = new[1]
            if s == '退出':
                nn = ''
                users_list = []
                del [idiom_dict[name]]
                return '已退出，下次想玩可以回复成语接龙或打开成语接龙！'
            if s == '下一个' or s == '换词':
                current_word = idiom_list[random.randint(0, len(idiom_list) - 1)]
                users_list = []
                nn = current_word
                users_list.append(current_word)
                idiom_dict[name] = nn, users_list
                return current_word
            else:
                wei = nn[len(nn) - 1]
                wei2 = lazy_pinyin(wei)
                shou = s[:1]
                shou2 = lazy_pinyin(shou)
                if wei2 != shou2:
                    return '亲！回答不正确哦~ 当前成语：' + nn
                else:
                    if s not in idiom_list:
                        res = s + ' 这不是一个成语哦~ 当前成语：' + nn
                        return res
                    else:
                        if s not in users_list:
                            try:
                                res_list = idiom_next_char(s, polyphone=True)
                                if s + ' 这不是一个成语哦' == res_list:
                                    return s + ' 这不是一个成语哦~ 当前成语：' + nn
                                else:
                                    for i in res_list:
                                        if users_list:
                                            for n in users_list:
                                                if n == i:
                                                    res_list.remove(i)
                                    nn = res_list[random.randint(0, len(res_list) - 1)]
                                    users_list.append(s)
                                    users_list.append(nn)
                                    idiom_dict[name] = nn, users_list
                                    print(nn, users_list)
                                    return nn
                            except Exception:
                                current_word = idiom_list[random.randint(0, len(idiom_list) - 1)]
                                users_list = []
                                nn = current_word
                                users_list.append(current_word)
                                idiom_dict[name] = nn, users_list
                                return u'接龙:是在下输了! 重新开始吧：' + nn
                        else:
                            return '亲，该词说过了，换个试试吧！ 当前成语：' + nn
        else:  # 直接说成语开始成语接龙
            users_list = []
            res_list = idiom_next_char(s, polyphone=True)
            if res_list:
                if type(res_list) is list:
                    nn = res_list[random.randint(0, len(res_list) - 1)]
                    users_list.append(nn)
                    idiom_dict[name] = nn, users_list
                    return nn
                else:
                    return ''
            else:
                return ''
    except Exception as e:
        print('成语接龙抱错', s, name, e)


# chengyujielong('', 'zufeng')
# chengyujielong('一心一意', 'zufeng')
# current_word = idiom_list[random.randint(0, len(idiom_list) - 1)]
# print(current_word)
# none_supply = idiom_next_char(current_word, polyphone=True)
# # none_supply = check_none_follow_list()
# print(none_supply, len(none_supply), type(none_supply))
# list = []
# for i in none_supply:
#     list.append(i)
# print(list)
# idiom_multi_char_length('刻舟求剑', polyphone=True)