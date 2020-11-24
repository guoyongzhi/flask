import numpy as np


class probability(object):
    @classmethod
    def probability_rob(cls):
        double_p = np.array([0.60, 0.29, 0.065, 0.033, 0.012])  # 设置奖励翻倍比例
        double = np.random.choice([1, 2, 3, 4, 5], p=double_p.ravel())
        return int(double)

    @classmethod
    def probability_reversal(cls):
        win_rate_p = np.array([0.8, 0.2])  # 设置成功失败比例（80%成功，20%被反）
        reversal = np.random.choice([0, 1], p=win_rate_p.ravel())
        return int(reversal)
