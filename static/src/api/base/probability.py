import numpy as np


class probability(object):
    @classmethod
    def probability_rob(cls):
        """
        打劫翻倍比例
        :return: 1, 2, 3, 4, 5
        :rtype: int
        """
        double_p = np.array([0.60, 0.29, 0.065, 0.033, 0.012])  # 设置奖励翻倍比例
        double = np.random.choice([1, 2, 3, 4, 5], p=double_p.ravel())
        return int(double)

    @classmethod
    def probability_reversal(cls):
        """
        打劫翻转比例
        :return: 0,1
        :rtype: int
        """
        win_rate_p = np.array([0.8, 0.2])  # 设置成功失败比例（80%成功，20%被反）
        reversal = np.random.choice([0, 1], p=win_rate_p.ravel())
        return int(reversal)
    
    @classmethod
    def probability_luck_draw(cls):
        """
        大转盘抽奖
        :return: 中奖结果，中奖额度，中奖类型
        :rtype: tuple
        """
        win_rate_p = np.array([0.4, 0.6])  # 设置抽奖比例
        reversal = np.random.choice([0, 1], p=win_rate_p.ravel())
        if reversal == 0:
            return "很遗憾未中奖，再接再厉吧！", 0, 0
        cb = np.random.choice([1, 2, 0])
        dd_list = ['金币', '积分', '打劫次数']
        if cb == 1:  # 积分
            d_list = [5, 10, 15, 20]
            win_rate_p = np.array([0.4, 0.35, 0.15, 0.1])
        elif cb == 2:  # 打劫次数
            d_list = [5, 10]
            win_rate_p = np.array([0.6, 0.4])
        else:  # 金币
            d_list = [2000, 4000, 6000, 8000, 10000]
            win_rate_p = np.array([0.4, 0.35, 0.15, 0.07, 0.03])
        reversal = np.random.choice(d_list, p=win_rate_p.ravel())
        return "恭喜中了" + dd_list[cb] + str(reversal), int(reversal), cb
    
    
if __name__ == '__main__':
    ass = probability.probability_luck_draw()
    print(ass)
