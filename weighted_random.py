#!/usr/bin/env python
# -*- coding=utf-8 -*-


import traceback
import time
import random
import bisect


class WeightedRandom(object):
    def __init__(self):
        # 备选项
        self.keys = list()
        # 备选项权重和列表
        self.weight_sums = list()
        # 备选项权重总和
        self.total_sum = 0.0

    # 显式释放内存
    def free(self):
        self.keys = list()
        self.weight_sums = list()

    # 设置队列权重
    def set_weight(self, weighted_item):
        """
        :type weighted_item: dict[object, float]
        """
        try:
            # 保存数据
            self.keys = list()
            for item in weighted_item.keys():
                self.keys.append(item)

            # 权重之和
            self.weight_sums = list()
            self.total_sum = 0.0
            for weight in weighted_item.values():
                self.total_sum += weight
                self.weight_sums.append(self.total_sum)
            return True
        except:
            print traceback.format_exc()
            return False

    # 加权随机选择
    def choice(self):
        try:
            r = random.random()
            weight_sum = r * self.total_sum
            idx = bisect.bisect_right(self.weight_sums, weight_sum)
            return self.keys[idx]
        except:
            print traceback.format_exc()
            return None


def __main__():
    rand = WeightedRandom()

    weighted_item = {
        1: 3,
        2: 1,
        3: 7,
        4: 100,
        5: 100,
        6: 300,
    }

    rand.set_weight(weighted_item)

    n = dict()
    l = list()
    x = time.time()
    for i in xrange(100000):
        v = rand.choice()
        l.append(v)
        if v not in n:
            n[v] = 0
        n[v] += 1
    print 'choose 100 data exhaust time: ', time.time() - x
    print weighted_item
    print n


if __name__ == '__main__':
    __main__()
