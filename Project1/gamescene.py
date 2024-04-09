# -*- coding: UTF-8 -*-
"""
@File ：gamescene.py
@Author ：Hry
@Date ：2024/04/09 10:47
@Intro: to create a class for the game scenes, including player/wall/box/hole, etc
"""

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
        init_box = data["box"] # [name/serial number/code, posx, posy]
        hole = data["hole"]    # [name/serial number/code, posx, posy]

        # goal: [ [0/1/2, boxname, hole.x, hole.y, direction] ] # 感觉用不上，可以删掉？
        goal = data["goal"]    

        init_player = data["player"]
        # 返回信息
        return mode, size, wall, init_box, hole, goal, init_player
    

    # 检查给定移动是否可行
    # 注意：该逻辑依赖于self.posBox，是在箱子推入洞口后不消失的设定下写的！！！
    # 如果箱子入洞后会消失，那么就应该对self.posBox进行处理，把消失的箱子去除掉
    def is_valid_move(self, move):
        currentMap = deepcopy(self.map) # 地图，此时只标识了wall
        for box in self.posBox:
            currentMap[box[1]][box[2]] = 2 # 标识box为2
        # print(currentMap) # debug        
        dst_x = self.posPlayer[0] + move[0]
        dst_y = self.posPlayer[1] + move[1]
        if currentMap[dst_x][dst_y] == 0: # player移动后的目标位置不是wall也不是box
            return True # 该写法依赖于move不超出地图的范围！且在wall包围的范围内！
        elif currentMap[dst_x][dst_y] == 2: # player移动后的目标位置是box
            x2 = self.posPlayer[0] + 2 * move[0] # player->box->下一个位置的x坐标
            y2 = self.posPlayer[1] + 2 * move[1]
            return currentMap[x2][y2] == 0
        else:
            pass


    # 获取角色可行的下一步动作
    def get_possible_moves(self):
        all_moves = [[-1, 0, 'u'], [1, 0, 'd'], [0, -1, 'l'], [0, 1, 'r']]
        possible_moves = []
        for move in all_moves:
            if self.is_valid_move(move): # 合法移动
                possible_moves.append(move)
        return possible_moves # 返回一个list


    # 显示游戏场景
    def DisplayScene(self):
        pass

    # 判断当前局面是否获胜，应当在每一步移动后判断一次
    def isSuccess(self):
        if self.mode == 0: # 箱子与洞口无对应关系
            box = [item[1:3] for item in self.posBox]
            hole = [item[1:3] for item in self.hole]
            return sorted(box) == sorted(hole)
        elif self.mode == 1: # 箱子与洞口一一对应，但是无方向之分
            return (self.posBox == self.hole)
        else: # 选做，箱子与洞口一一对应，并且只能从指定方向进入
            # 在判断是否成功这方面，应该和mode == 1是一样的？
            pass

    # 判断是否进入了死局，应当在每一步移动后判断一次
    def isDeadend(self):
        pass
    
    # 执行移动操作，目标动作是action
    # 调用此函数时，默认action已经是经过检验的合法的行动
    def Move(self, action): # action:[1,0,'d']
        # 更新player位置 posPlayer:[2,1]
        self.posPlayer[0] += action[0]
        self.posPlayer[1] += action[1]
        for index, posB in enumerate(self.posBox):
            # posB: ['a',2,2]
            if posB[1:3] == self.posPlayer: # 推动箱子
                self.posBox[index][1] += action[0]
                self.posBox[index][2] += action[1]
                break

    
    # 处理键盘的输入keystroke
    # 此处输入的参数keystroke并不是键盘按键，是已经处理过的{'u','d','l','r'}之一
    def from_keyboard(self, keystroke):
        legal_in = ['u', 'd', 'l', 'r'] # 合法输入
        legal_out = [[-1, 0, 'u'], [1, 0, 'd'], [0, -1, 'l'], [0, 1, 'r']] # 合法输出
        return legal_out[legal_in.index(keystroke.lower())] # 使之对大小写不敏感




