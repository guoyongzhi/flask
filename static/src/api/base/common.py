

def get_nickname(number):
    if number > 200000:
        ty = '大富翁'
    elif number > 100000:
        ty = '大老板'
    elif number > 10000:
        ty = '小老板'
    elif number > 5000:
        ty = '小康生活'
    elif number > 1000:
        ty = '小有成就'
    else:
        ty = '新手上路'
    return ty


def is_talk_keyword(talk='', keyword=[]):
    """
    判断话语是否是关键字
    :param talk: 话语
    :type talk: str
    :param keyword: 关键字
    :type keyword: list
    :return: 是否存在
    :rtype: bool
    """
    for key in keyword:
        if talk == key:
            return True
    return False
