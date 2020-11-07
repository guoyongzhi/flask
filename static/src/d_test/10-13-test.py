talk = '@哈哈哈ꉂꉂ(ᵔᗜᵔ*)  1'
Users_list = ['哈哈哈ꉂꉂ(ᵔᗜᵔ*)', '赣D-自豪红-邦 ', '赣B-雪域白-内涵段子', '桂N精英白-萝岗']

if '@' in talk:
    # 拆分语言
    now_talk = talk.split('@')
    if now_talk[0] == '':
        del now_talk[0]
    # if len(now_talk) == 1:
    #     return ""  # 没有说话直接返回
    whoUserName = ''
    if talk[:1] == '@':  # 艾特一人（首位）
        try:
            new = talk.split()
            who = new[0]
            who = who[1:]
        except Exception as e:
            print('报错了', e)
        dd = 0
        ss = 0
        try:
            if Users_list:
                while ss <= len(new):
                    for i in Users_list:
                        t_name = i
                        if t_name == who:
                            dd = 1
                            break
                    if dd == 1:
                        break
                    else:
                        ss += 1
                        if ss >= len(new):
                            break
                        joint_name = who + ' '
                        a = 1
                        ao = 0
                        d = 0
                        while ao <= 10:
                            ll = len(joint_name) + 1
                            if talk[:ll] == '@' + joint_name:
                                who = joint_name
                                break
                            else:
                                if d == 0:
                                    joint_name = who + new[ss-1]
                                    d += 1
                                    ss -= 1
                                else:
                                    nn = ' '
                                    for i in range(0, a):
                                        nn += ' '
                                    joint_name = who + nn + new[ss]
                                    a += 1
                                    ao += 1
            else:
                who = ''
                print('找不到用户', 111)
        except Exception as eb:
            who = ''
            print('处理用户抱错了', eb, 213)
        try:
            print(ss)
            if ss < len(new):
                if ss != len(new):
                    if ss == 0:
                        ss += 1
                    talk = ''
                    for i in range(ss, len(new)):
                        if talk == '':
                            talk = talk + new[i]
                        else:
                            talk = talk + ' ' + new[i]
                else:
                    talk = new[ss]
            else:
                talk = ''
        except Exception as ec:
            print(ec, 124)
            talk = ''  # print(ss, '----')
    elif len(now_talk) > 3:  # 处理艾特多人（先不处理）
        print(999)
    else:  # 艾特一人（话语在首位）
        try:
            a_talk = now_talk
            b_talk = a_talk[0]
            who = a_talk[1]
            if '' in who:
                now_talk = who.split()
                who = now_talk[0]

        except Exception as e:
            print('报错了', e)
        dd = 0
        ss = 0
        try:
            if Users_list:
                while ss <= len(now_talk):
                    for i in Users_list:
                        t_name = i
                        if t_name == who:
                            dd = 1
                            break
                    if dd == 1:
                        break
                    else:
                        ss += 1
                        if ss >= len(now_talk):
                            break
                        joint_name = who + ' '
                        a = 1
                        ao = 0
                        d = 0
                        while ao <= 10:
                            ll = len(b_talk) + len(joint_name) + 1
                            if talk[:ll] == b_talk + '@' + joint_name:
                                who = joint_name
                                break
                            else:
                                if d == 0:
                                    joint_name = who + now_talk[ss - 1]
                                    d += 1
                                    ss -= 1
                                else:
                                    nn = ' '
                                    for i in range(0, a):
                                        nn += ' '
                                    joint_name = who + nn + now_talk[ss]
                                    a += 1
                                    ao += 1
            else:
                who = ''
                print('找不到用户', 222)
        except Exception as eb:
            who = ''
            print('处理用户抱错了', eb, 333)
        try:
            if ss < len(now_talk):
                if ss != len(now_talk):
                    if ss == 0:
                        ss += 1
                    talk = ''
                    for i in range(ss, len(now_talk)):
                        if talk == '':
                            talk = talk + now_talk[i]
                        else:
                            talk = talk + ' ' + now_talk[i]
                else:
                    talk = now_talk[ss]
            else:
                talk = ''
            talk = b_talk + talk  # print(talk)
        except Exception as ec:
            print(ec, 444)
            talk = ''

print('----' + who + '---' + talk)
