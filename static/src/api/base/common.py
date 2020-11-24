

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
