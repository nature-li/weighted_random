#!/usr/bin/env python
# -*- coding=utf-8 -*-


import traceback
import numpy
import time
import random
import bisect
import copy
from gevent import lock


class WeightedRandom(object):
    def __init__(self):
        self.keys = list()
        self.weight_sums = list()
        self.sem = lock.BoundedSemaphore(1)

    # 设置队列权重
    def set_weight(self, weighted_item):
        """
        :type weighted_item: dict[object, float]
        """
        try:
            # 保存数据
            self.keys = copy.deepcopy(weighted_item.keys())

            # 调权，使之总和为1.0
            weights = list()
            for weight in weighted_item.values():
                weights.append(float(weight))
            props = numpy.array(weights)
            props /= props.sum()

            # 权重之和排序
            self.weight_sums = list()
            for i in xrange(1, len(props) + 1):
                weight_sum = props[0: i].sum()
                self.weight_sums.append(weight_sum)
            return True
        except:
            print traceback.format_exc()
            return False

    # 加权随机选择
    def choice(self):
        try:
            r = random.random()
            idx = bisect.bisect_right(self.weight_sums, r)
            return self.keys[idx]
        except:
            print traceback.format_exc()
            return None


class DoubleRandom(object):
    def __init__(self):
        self.double_random = {
            0: WeightedRandom(),
            1: WeightedRandom()
        }
        self.using_idx = 0
        self.sem = lock.BoundedSemaphore(1)

    # 获取加权随机数
    def choice(self):
        try:
            # 选取正在使用中的random
            self.sem.acquire()
            using_idx = self.using_idx
            self.sem.release()

            using_random = self.double_random[using_idx]
            """:type: WeightedRandom"""

            # 获取加权随机数
            value = using_random.choice()
            return value
        except:
            print traceback.format_exc()
            return None

    # 设置权重
    def set_weight(self, weighted_item):
        try:
            # 获取未投入使用的random
            self.sem.acquire()
            unused_idx = (self.using_idx + 1) % 2
            self.sem.release()

            # 设置这个准备使用的random
            unused_random = self.double_random[unused_idx]
            unused_random.set_weight(weighted_item)

            # 将设置好的random投入使用
            self.sem.acquire()
            self.using_idx = unused_idx
            self.sem.release()
            return True
        except:
            print traceback.format_exc()
            return False


def __main__():
    rand = DoubleRandom()

    weighted_item = dict()
    for i in range(91, 100 + 1):
        weighted_item[i] = 100

    for i in range(1, 91):
        weighted_item[i] = 1

    x = time.time()
    rand.set_weight(weighted_item)
    print 'init_weight exhaust time: ', time.time() - x

    n = dict()
    l = list()
    x = time.time()
    for i in range(1000):
        v = rand.choice()
        l.append(v)
        if v not in n:
            n[v] = 0
        n[v] += 1
    print 'choose 100 data exhaust time: ', time.time() - x
    print n


if __name__ == '__main__':
    __main__()


