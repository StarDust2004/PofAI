# -*- coding: UTF-8 -*-
"""
@File : node.py
@Author ：Hry
@Date ：2024/04/16 22:37
@Intro: a* search
@Modify: 
"""

from node import Node
from utils import *
from gamescene import GameScene
import time

def AStarSearch(problem: GameScene):
    # param problem: 一个游戏场景，包含布局、箱子、玩家、洞口等信息
    player = problem.init_player # 玩家位置
    box = problem.init_box # 箱子位置
    node_init = Node(box, player) # 初始化节点/根节点

    if problem.isSuccess(node_init.posBox):
        return node_init

    open = PriorityQueue(node_init, problem) # 开节点表,优先队列
    closed = Set() # 闭节点表，集合(自定义)

    while not open.empty():
        node = open.pop()
        closed.add(node)
        posPlayer = node.posPlayer # 当前节点的Player位置
        posBox = node.posBox # 当前节点的box位置列表
        actions = problem.get_possible_moves(posBox, posPlayer) # 当前节点可采取的行动
        for action in actions:
            # 采取一步行动后，新的player位置和box位置列表
            new_Player, new_Box = problem.Move(action, posBox, posPlayer)
            new_node = node.child_node(new_Box, new_Player, action) # node的子节点
            if problem.isSuccess(new_Box): # 新节点已经达成终局-成功
                return new_node
            if problem.isDeadend(new_Box): # 新节点已经达成终局-死局
                closed.add(new_node) # 直接剪枝（放入闭节点表，不再拓展）
            elif not open.find(new_node) and not closed.find(new_node): # 不在开节点表也不在闭节点表
                open.push(new_node) # 放入开节点表，以备后续拓展
            elif open.find(new_node): # 在开节点表里
                open.compare_and_replace(open.find(new_node), new_node) # 更优则替换
            else:
                pass 
    
    return None

def hash_state(): # 在open和closed里面存放状态的哈希值，而不是整个Node节点
    # 状态由玩家位置和箱子位置列表共同表示（Node判等用的是这两个）
    pass

# 搜索算法测试
if __name__ == '__main__':
    scene1 = GameScene("demo0.json")
    start_time = time.time() # 开始时间
    final_node = AStarSearch(scene1)
    end_time = time.time() # 结束时间

    time_cost = end_time - start_time # 用时
    print(f'time cost:{time_cost}')
    final_node.path_action_print()
    print(f'\ndepth:{final_node.path_cost}')

            





