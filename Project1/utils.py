# -*- coding: UTF-8 -*-
"""
@File : node.py
@Author ：Hry
@Date ：2024/04/16 22:39
@Intro: to create Queue, PriorityQueue and so on
@Modify: 
"""
# 实现了Queue、PriorityQueue、Stack、Set、Dict等自定义类

from collections import deque
import sortedcontainers
from gamescene import GameScene


# 队列（deque右进左出）
class Queue(object):
    def __init__(self):
        self._items = deque([])
    
    def push(self, item):
        self._items.append(item) # 在双端队列右端增加

    def pop(self):
        if not self.empty():
            return self._items.popleft() # 移除并返回Deque左端的元素
        else:
            return None

    def empty(self): # 队列是否为空
        return len(self._items) == 0

    def qsize(self): # 队列长度
        return len(self._items)

    def find(self, item):
        if item in self._items:
            return self._items.index(item)
        else:
            return None


class Stack(object):
    def __init__(self):
        self._items = list()

    def empty(self): # 栈是否为空
        return len(self._items) == 0
    
    def push(self, item): # 压入元素到末尾
        self._items.append(item)

    def pop(self): # 从栈顶移除并返回最后一个元素
        if not self.empty():
            return self._items.pop() # 返回列表末端元素 
        else:
            return None
        
    def __len__(self): # 栈的长度
        return len(self._items)


# 优先级队列
class PriorityQueue(object):
    def __init__(self, node, problem: GameScene): # 默认按照prior升序排列
        self._queue = sortedcontainers.SortedList([node],key=lambda item:item.Prior(problem))

    def push(self, node): # 添加到有序列表中
        self._queue.add(node)

    def pop(self): # 弹出第一个节点
        return self._queue.pop(index=0)

    def empty(self): # 检查优先级队列是否为空
        return len(self._queue) == 0

    # 比较并替换节点
    def compare_and_replace(self, i:int, node):
        # if node < self._queue[i]: # Node.__lt__ # 如果新节点node更优
        if node.__lt__(self._queue[i]):
            self._queue.pop(index=i)
            self._queue.add(node) # 则替换掉原先那个节点

    # 查找节点
    def find(self, node):
        try:
            loc = self._queue.index(node)
            return loc
        except ValueError:
            return None


class Set(object):
    def __init__(self):
        self._items = set()

    def add(self, item):
        self._items.add(item)

    def remove(self, item):
        self._items.remove(item)

    def find(self, item):
        return item in self._items


class Dict(object):
    def __init__(self):
        self._items = dict()

    def add(self, key, value):
        self._items.update({key: value})

    def remove(self, key):
        self._items.pop(key, None)

    def find(self, key):
        return self._items[key] if key in self._items else None


