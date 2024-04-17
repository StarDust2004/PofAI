# -*- coding: UTF-8 -*-
"""
@File ：gamescene.py
@Author ：Hry
@Date ：2024/04/09 10:47
@Intro: to create a class for the game scenes, including player/wall/box/hole, etc
@Modify: 2024/04/10? remove posBox and posPlayer from GameScene's property, \
    resuming that they shall not be part of this class
"""
# DisplayScene()还未完成
# self.posBox / self.posPlayer还在被各个函数使用，但它们不应该作为类的元素存在;
# 后续希望去除这两个变量，在其他调用这个类的函数中维护posBox(list)和posPlayer(二元list)
# 而对本类中的各个函数传入posBox和posPlayer。
# 新增了PrintMap，用于调试时观察局面改变

import numpy as np
import json
from copy import deepcopy
import pygame


class GameScene:
    # map_json:可能存在的json文件，从json文件读取地图场景
    # info：列表/字典？，形如json文件中的内容，给出地图场景设置
    def __init__(self, map_json = None, info = None):
        if map_json != None:
            self.mode, self.size, self.wall, self.init_box, self.hole, self.goal, \
                self.init_player = self.ReadFromJson(map_json)
        else:
            self.mode, self.size, self.wall, self.init_box, self.hole, self.goal, \
                self.init_player = info
        # 以下二者是会改变的，所以不应该作为该类的属性
        self.posBox = self.init_box # 游戏过程中移动后的箱子位置列表
        self.posPlayer = self.init_player # 角色位置（用列表表示的一个二元组合）eg:[1,1]
        # 箱子数量
        self.numofbox = len(self.init_box) # ?
        # 构建一个地图，便于判断合理性
        self.map = np.zeros([self.size[0],self.size[1]])
        for pos in self.wall:
            self.map[pos[0],pos[1]] = 1 # 1为wall；此后会标记box为2。

    # staticmethod:装饰器，用于将方法标记为静态方法。
    # 静态方法不需要访问类的实例，因此不会自动传递类或实例的引用。
    # 静态方法可以在不实例化类的情况下调用，并且不会隐式传递类或实例。
    # 因此，静态方法只能访问类的属性和方法，而不能访问实例的属性和方法。
    @staticmethod
    def ReadFromJson(map_json):
        with open(map_json, 'r') as f: # 打开json文件
            data = json.load(f)
        # 从json数据中获取信息
        mode = data["mode"]
        size = data["size"]
        wall = data["wall"]
        # init_box = data["box"] # [name/serial number/code, posx, posy]
        init_box = sorted(data["box"], key = lambda x:x[0]) # 按照box的序号重新排好序
        # hole = data["hole"]    # [name/serial number/code, posx, posy]
        hole = sorted(data["hole"], key = lambda x:x[0]) # 按照hole的序号重新排好序
        # debugging
        print("init_boxes:", init_box)
        print("holes:", hole)


        # goal: [ [0/1/2, boxname, hole.x, hole.y, direction] ] # 感觉用不上，可以删掉？
        goal = data["goal"]    

        init_player = data["player"]
        # 返回信息
        return mode, size, wall, init_box, hole, goal, init_player
    

    # 检查给定移动是否可行
    # 注意：该逻辑依赖于self.posBox，是在箱子推入洞口后不消失的设定下写的！！！（已解决）
    # 该逻辑依赖于posBox和self.hole严格按照顺序一一对应地排列
    # 如果箱子入洞后会消失，那么就应该对self.posBox进行处理，把消失的箱子去除掉
    def is_valid_move(self, move, posBox, posPlayer):
        currentMap = deepcopy(self.map) # 地图，此时只标识了wall
        # for box in posBox:
        for index, box in enumerate(posBox):
            if self.mode == 1: # 箱子进洞后会消失，只留下一个不影响其他箱子通过的洞
                # 这里假设posBox和self.hole都是按照序号'a''b''c'这样排好序的
                if box == self.hole[index]: # 箱子已经在对应的洞口里面了
                    continue # 对这个位置不做处理（这个位置不会对其他箱子造成任何影响）
                else: # 箱子不在洞口里
                    currentMap[box[1]][box[2]] = 2 # 标识box为2
            elif self.mode == 0: # 箱子与洞口没有对应关系，且进洞后不会消失
                currentMap[box[1]][box[2]] = 2 # 标识box为2
            else:
                pass
        # if self.mode == 1: # 箱子推进洞口后会消失
        #     for hole in self.hole:
        #         if currentMap[hole[1]][hole[2]] == 2: # 
        #             currentMap[hole[1]][hole[2]] = 0 # 空地
        # print(currentMap) # debug        
        dst_x = posPlayer[0] + move[0]
        dst_y = posPlayer[1] + move[1]
        if currentMap[dst_x][dst_y] == 0: # player移动后的目标位置不是wall也不是box
            return True # 该写法依赖于move不超出地图的范围！且在wall包围的范围内！
        elif currentMap[dst_x][dst_y] == 2: # player移动后的目标位置是box
            x2 = posPlayer[0] + 2 * move[0] # player->box->下一个位置的x坐标
            y2 = posPlayer[1] + 2 * move[1]
            return currentMap[x2][y2] == 0
        else:
            pass


    # 获取角色可行的下一步动作
    def get_possible_moves(self, posBox, posPlayer):
        all_moves = [[-1, 0, 'u'], [1, 0, 'd'], [0, -1, 'l'], [0, 1, 'r']]
        possible_moves = []
        for move in all_moves:
            if self.is_valid_move(move, posBox, posPlayer): # 合法移动
                possible_moves.append(move)
        return possible_moves # 返回一个list


    # 显示游戏场景
    def DisplayScene(self):
        pass


    # 计算启发函数值：当前节点（给定节点）到目标节点最小路径代价的估计值
    def Heuristic_func(self, posBox):
        posHole = self.hole # 洞口位置列表
        cost = 0 # 路径代价
        # param: posBox - 箱子位置列表
        if self.mode == 1: # mode == 1, 箱子与洞口一一对应
            for i in range(0, self.numofbox): # h(n) = 曼哈顿距离之和
                cost += np.abs(posBox[i][1] - posHole[i][1]) + np.abs(posBox[i][2] - posHole[i][2])
        elif self.mode == 0: # 箱子与洞口无一一对应关系
            # x方向上的最小曼哈顿距离之和 + y方向上的最小曼哈顿距离之和 <= 实际情况 -> 可采纳
            box_x = sorted(i[1] for i in posBox) # box 在x方向上排序
            box_y = sorted(i[2] for i in posBox)
            hole_x = sorted(i[1] for i in posHole) # hole在x方向上排序
            hole_y = sorted(i[2] for i in posHole)
            for i in range(0, self.numofbox):
                cost += np.abs(box_x[i] - hole_x[i]) + np.abs(box_y[i] - hole_y[i])
        else: # 可能的其他情况
            pass
        return cost


    # 调试和测试时用的，只是简单打出矩阵
    def PrintMap(self, posBox, posPlayer, posHole):
        if self.mode == 0: # 洞口与箱子无对应关系
            TheMap = deepcopy(self.map)
            for box in posBox:
                TheMap[box[1]][box[2]] += 2 # 标识box为2
            for hole in posHole:
                TheMap[hole[1]][hole[2]] += 3
            TheMap[posPlayer[0]][posPlayer[1]] += 10
            print(TheMap)
        elif self.mode == 1: # 洞口与箱子一一对应，但无方向差别
            TheMap = deepcopy(self.map)
            # for index, box in enumerate(posBox):
            #     TheMap[box[1]][box[2]] = 101 + index # 箱子和序号
            # for index, hole in enumerate(posHole):
            #     TheMap[hole[1]][hole[2]] = 201 + index
            for index, box in enumerate(posBox):
                if box != self.hole[index]: #箱子不在对应的洞里面
                    TheMap[box[1]][box[2]] += 10 + ord(box[0]) - 96 # 显示
            for hole in posHole:
                TheMap[hole[1]][hole[2]] += 100 + ord(hole[0]) - 96
            TheMap[posPlayer[0]][posPlayer[1]] += 500
            print(TheMap)


    # 判断当前局面是否获胜，应当在每一步移动后判断一次
    def isSuccess(self, posBox):
        if self.mode == 0: # 箱子与洞口无对应关系
            box = [item[1:3] for item in posBox]
            hole = [item[1:3] for item in self.hole]
            return sorted(box) == sorted(hole)
        elif self.mode == 1: # 箱子与洞口一一对应，但是无方向之分
            return (posBox == self.hole)
        else: # 选做，箱子与洞口一一对应，并且只能从指定方向进入
            # 在判断是否成功这方面，应该和mode == 1是一样的？
            pass

    # 判断是否进入了死局，应当在每一步移动后判断一次
    # 只在当前局势下判断是否出现了死锁，而不考虑在移动一步或几步后、是否其实已经是最终无解了
    def isDeadend(self, posBox): # posBox为当前箱子位置列表
        currentMap = deepcopy(self.map) # 当前地图，此时只标识了wall

        # for box in posBox:
        #     currentMap[box[1]][box[2]] = 2 # 标识box为2
        if self.mode == 0: # 不对应，且进洞不消失
            for box in posBox:
                currentMap[box[1]][box[2]] = 2 # 标识box为2
        elif self.mode == 1: # 一一对应，且箱子进洞即消失
            for index, box in enumerate(posBox):
                if box != self.hole[index]: # 还未进入对应洞口的箱子
                    currentMap[box[1]][box[2]] = 2 # 标识box为2
                else:
                    continue
        else:
            pass

        pos_hole = [i[1:3] for i in self.hole]
        for box in posBox:
            if box[1:3] not in pos_hole: # 此箱子还未入洞
                # 待检查的区域
                area = [ [box[1]-1, box[2]-1], [box[1]-1, box[2]], [box[1]-1, box[2]+1],\
                               [box[1], box[2]-1],   [box[1], box[2]],   [box[1], box[2]+1]  ,\
                               [box[1]+1, box[2]-1], [box[1]+1, box[2]], [box[1]+1, box[2]+1] ]
                # 墙角情形 * 4
                if currentMap[area[1][0]][area[1][1]] == 1 and currentMap[area[3][0]][area[3][1]] == 1:
                    return True
                elif currentMap[area[1][0]][area[1][1]] == 1 and currentMap[area[5][0]][area[5][1]] == 1:
                    return True
                elif currentMap[area[3][0]][area[3][1]] == 1 and currentMap[area[7][0]][area[7][1]] == 1:
                    return True
                elif currentMap[area[5][0]][area[5][1]] == 1 and currentMap[area[7][0]][area[7][1]] == 1:
                    return True
                # 四块情形 * n（4种方位）
                elif currentMap[area[0][0]][area[0][1]] > 0 and currentMap[area[1][0]][area[1][1]] > 0 and \
                      currentMap[area[3][0]][area[3][1]] > 0:
                    return True
                elif currentMap[area[1][0]][area[1][1]] > 0 and currentMap[area[2][0]][area[2][1]] > 0 and \
                      currentMap[area[5][0]][area[5][1]] > 0:
                    return True
                elif currentMap[area[3][0]][area[3][1]] > 0 and currentMap[area[6][0]][area[6][1]] > 0 and \
                      currentMap[area[7][0]][area[7][1]] > 0:
                    return True
                elif currentMap[area[5][0]][area[5][1]] > 0 and currentMap[area[7][0]][area[7][1]] > 0 and \
                      currentMap[area[8][0]][area[8][1]] > 0:
                    return True
                # “之”字形 * 8
                elif currentMap[area[0][0]][area[0][1]] == 1 and currentMap[area[3][0]][area[3][1]] == 2 and \
                      currentMap[area[7][0]][area[7][1]] == 1:
                    return True
                elif currentMap[area[1][0]][area[1][1]] == 1 and currentMap[area[5][0]][area[5][1]] == 2 and \
                      currentMap[area[8][0]][area[8][1]] == 1:
                    return True
                elif currentMap[area[0][0]][area[0][1]] ==1 and currentMap[area[1][0]][area[1][1]] == 2 and \
                      currentMap[area[5][0]][area[5][1]] == 1:
                    return True
                elif currentMap[area[3][0]][area[3][1]] == 1 and currentMap[area[7][0]][area[7][1]] == 2 and \
                      currentMap[area[8][0]][area[8][1]] == 1:
                    return True
                elif currentMap[area[1][0]][area[1][1]] == 1 and currentMap[area[3][0]][area[3][1]] == 2 and \
                      currentMap[area[6][0]][area[6][1]] == 1:
                    return True
                elif currentMap[area[2][0]][area[2][1]] == 1 and currentMap[area[5][0]][area[5][1]] == 5 and \
                      currentMap[area[7][0]][area[7][1]] == 1:
                    return True
                elif currentMap[area[2][0]][area[2][1]] == 1 and currentMap[area[1][0]][area[1][1]] == 2 and \
                      currentMap[area[3][0]][area[3][1]] == 1:
                    return True
                elif currentMap[area[5][0]][area[5][1]] == 1 and currentMap[area[7][0]][area[7][1]] == 2 and \
                      currentMap[area[6][0]][area[6][1]] == 1:
                    return True
                else: # 可能还有其他未考虑到的情况
                    pass
        return False # 未出现任何一种死锁情况，返回False，表示尚未陷入死局
                


    
    # 执行移动操作，目标动作是action
    # 调用此函数时，默认action已经是经过检验的合法的行动
    # def Move(self, action, posBox, posPlayer): # action:[1,0,'d']
    #     # 更新player位置 posPlayer:[2,1]
    #     posPlayer[0] += action[0]
    #     posPlayer[1] += action[1]
    #     if self.mode == 0: # 箱子与洞口无对应关系，且箱子入洞后不消失
    #         for index, posB in enumerate(posBox):
    #             # posB: ['a',2,2]
    #             if posB[1:3] == posPlayer: # 推动箱子
    #                 posBox[index][1] += action[0]
    #                 posBox[index][2] += action[1]
    #                 break
    #     elif self.mode == 1: # 箱子与洞口一一对应，且箱子入洞后消失
    #         for index, posB in enumerate(posBox):
    #             # posB: ['a',2,2]
    #             if posB[1:3] == posPlayer and posB != self.hole[index]: # 箱子不在洞里，方可推动箱子
    #                 posBox[index][1] += action[0]
    #                 posBox[index][2] += action[1]
    #                 break
    def Move(self, action, posBox, posPlayer): # action:[1,0,'d']
        # 更新player位置 posPlayer:[2,1]
        px = posPlayer[0] + action[0]
        py = posPlayer[1] + action[1]
        posP = [px, py] # 新的Player位置
        posB = [] # 用来存新的箱子位置
        if self.mode == 0: # 箱子与洞口无对应关系，且箱子入洞后不消失
            for index, box in enumerate(posBox): # posB: ['a',2,2]
                if box[1:3] == posP: # 需要推走箱子
                    bx = box[1] + action[0]
                    by = box[2] + action[0]
                    new_box = [box[0], bx, by]
                else:
                    new_box = box
                posB.append(new_box)
        elif self.mode == 1: # 箱子与洞口一一对应，且箱子入洞后消失
            for index, box in enumerate(posBox): # posB: ['a',2,2]
                if box[1:3] == posP and box != self.hole[index]: # 箱子不在洞里，方可推动箱子
                    bx = box[1] + action[0]
                    by = box[2] + action[1]
                    new_box = [box[0], bx, by]
                else:
                    new_box = box
                posB.append(new_box)

        return posP, posB # 返回移动后，玩家和箱子坐标列表

    
    # 处理键盘的输入keystroke，合法性必须在传入前得到确认
    # 此处输入的参数keystroke并不是键盘按键，是已经处理过的{'u','d','l','r'}之一
    def from_keyboard(self, keystroke):
        legal_in = ['u', 'd', 'l', 'r'] # 合法输入
        legal_out = [[-1, 0, 'u'], [1, 0, 'd'], [0, -1, 'l'], [0, 1, 'r']] # 合法输出
        return legal_out[legal_in.index(keystroke.lower())] # 使之对大小写不敏感




