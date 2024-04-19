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


# 同时维护两个开节点表，一个存节点，一个存哈希值，简化查找等操作
def AStarSearch(problem: GameScene):
    # param problem: 一个游戏场景，包含布局、箱子、玩家、洞口等信息
    player = problem.init_player # 玩家位置
    box = problem.init_box # 箱子位置
    node_init = Node(box, player) # 初始化节点/根节点

    if problem.isSuccess(node_init.posBox):
        return node_init

    open_q = PriorityQueue(node_init, problem) # 开节点表(用来存放节点node！),优先队列
    open_set = Set() # 开节点表（用来存放节点的哈希值）,集合,方便查找等操作
    closed = Set() # 闭节点表,集合(自定义)

    node_init_hashed = hash_state(problem.mode, node_init.posBox, node_init.posPlayer)
    open_set.add(node_init_hashed) # 初始节点哈希值，进入open_set

    while not open_q.empty(): # 开节点表非空
        node = open_q.pop()
        node_hashed = hash_state(problem.mode, node.posBox, node.posPlayer) # node的哈希值
        closed.add(node_hashed) # node哈希值，进入闭节点表closed
        posPlayer = node.posPlayer # 当前节点的Player位置
        posBox = node.posBox # 当前节点的box位置列表
        actions = problem.get_possible_moves(posBox, posPlayer) # 当前节点可采取的行动
        for action in actions:
            # 采取一步行动后，新的player位置和box位置列表
            new_Player, new_Box = problem.Move(action, posBox, posPlayer)
            new_node = node.child_node(new_Box, new_Player, action) # node的子节点
            new_node_hashed = hash_state(problem.mode, new_node.posBox, new_node.posPlayer) # 新节点的哈希值
            if problem.isSuccess(new_Box): # 新节点已经达成终局-成功
                return new_node
            if problem.isDeadend(new_Box): # 新节点已经达成终局-死局
                closed.add(new_node_hashed) # 直接剪枝（放入闭节点表，不再拓展）
            elif not open_set.find(new_node_hashed) and not closed.find(new_node_hashed): # 不在开节点表也不在闭节点表
                open_q.push(new_node) # 放入开节点表，以备后续拓展
                open_set.add(new_node_hashed) # 哈希值也放入开节点表
            # elif open_set.find(new_node_hashed): # 在开节点表里
            #     if open_q.find(new_node) != None:
            #         open_q.compare_and_replace(open_q.find(new_node), new_node) # 更优则替换
            else:
                pass 
    
    return None

def hash_state(mode, posBox, posPlayer) -> str: # 在open和closed里面存放状态的哈希值，而不是整个Node节点
    # 状态由玩家位置和箱子位置列表共同表示（Node判等用的是这两个）
    # 区分mode = 0/1，mode = 0箱子位置是无序的，为了哈希就要先把箱子位置排好序
    # mode = 1箱子位置是有序的，直接哈希即可
    ppx = posPlayer[0] # 玩家x坐标
    ppy = posPlayer[1] # 玩家y坐标
    list = [ppx, ppy] # 准备转换为str类型的内容
    if mode == 0: # 无对应关系：箱子位置无序
        Box = [i[1:3] for i in posBox] # 先提取出箱子列表中的坐标(无序->名称不重要)
        Box_sorted = sorted(Box) # 先把box按照（先x后y、升序）的顺序排好序
        for box in Box_sorted: # 再依次把所有箱子的x坐标、y坐标加入list
            list.append(box[0])
            list.append(box[1])
    elif mode == 1: # 一一对应：箱子位置有序
        for box in posBox: # 直接依次把所有箱子的x坐标、y坐标加入list即可
            list.append(box[1])
            list.append(box[2])
    else:
        pass
    str_list = map(str,list)
    list_hash = ''.join(str_list) # 转换为可哈希的字符串
    return list_hash



# 搜索算法测试
if __name__ == '__main__':
    # scene1 = GameScene("jsonMaps/mode1_3.json")
    scene1 = GameScene('jsonMaps/mode0_3.json')
    print("mode:", scene1.mode)
    scene1.PrintMap(scene1.init_box, scene1.posPlayer, scene1.hole)
    start_time = time.time() # 开始时间
    final_node = AStarSearch(scene1)
    end_time = time.time() # 结束时间

    time_cost = end_time - start_time # 用时
    print(f'time cost:{time_cost}s')
    print("movement path:", end = ' ')
        
    actions = final_node.path_action_print() # 打印路径
    # final_node.pathprint()
    # print(final_node)
    print(f'\ndepth/steps:{final_node.path_cost}') # 深度/步数

    # path = final_node.path()
    # for node in path:
    #     scene1.PrintMap(node.posBox, node.posPlayer, scene1.hole) # 各步骤后的地图

    # print(actions)
    # for a in actions:
    #     action = scene1.from_keyboard(a)
    #     if scene1.is_valid_move(action, posBox, posPlayer):
    #         posPlayer, posBox = scene1.Move(action, posBox, posPlayer)
    #         print(posBox)
    #         print(posPlayer) 
    #         scene1.PrintMap(posBox, posPlayer, scene1.hole)

            





