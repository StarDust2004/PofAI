"""
# File       : UItest.py
# Time       ：2024/4/18 1:49
# Author     ：Hry
# Description：to test how to set ui for the game
"""


from collections import deque
import pygame, sys, os, time
from pygame.locals import *
# from search import AStarSearch
from gamescene import GameScene
import time


# 初始化pygame
pygame.init()
# 加载各项游戏资源（异常处理）
# gameicon = pygame.image.load("basic-pics/BoxIcon.png") # 设置游戏图标
# pygame.display.set_icon(gameicon) # 展示游戏图标
screen = pygame.display.set_mode((600,600)) # 设置主界面大小
# 绘制游戏窗口
# screen.fill(skin.get_at((0, 0)))

# blank = pygame.image.load("pictures/exp_pics/space.png").convert() # 空格
# player = pygame.image.load("pictures/exp_pics/mouse.png").convert() # 老鼠
# box = pygame.image.load("pictures/exp_pics/egg.png").convert() # 鸡蛋
# wall = pygame.image.load("pictures/exp_pics/wall.png").convert() # 墙
# hole = pygame.image.load("pictures/exp_pics/hole.png").convert() # 洞口
# boxinhole = pygame.image.load("pictures/exp_pics/egginhole.png").convert()  # 鸡蛋在洞

blank = pygame.image.load("pictures/40pixels/blank.png").convert() # 空格
player = pygame.image.load("pictures/40pixels/player.png").convert() # 老鼠
box = pygame.image.load("pictures/40pixels/box.png").convert() # 鸡蛋
wall = pygame.image.load("pictures/40pixels/wall.png").convert() # 墙
hole = pygame.image.load("pictures/40pixels/hole.png").convert() # 洞口
boxinhole = pygame.image.load("pictures/40pixels/box_in_hole.png").convert()  # 鸡蛋在洞

clock = pygame.time.Clock()                         #  游戏刷新速度（我个人这么理解）

start_ck = pygame.Surface(screen.get_size())    #   充当开始界面的画布
start_ck = start_ck.convert()
start_ck.fill((128,128,128))  # 白色画布1（开始界面用的）

n1 = True
while n1:
    clock.tick(30)
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 用户按下了Escape按键，则退出游戏进程循环
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    scene1 = GameScene("jsonMaps/mode1_1.json")
    scene1.DisplayScene(scene1.posBox, scene1.posPlayer, screen, blank, player, box, wall, hole, boxinhole)
    pygame.display.update()

    while scene1.isSuccess(posBox) != True:
        a = input("choose a direction:")
        if a == 'q':
            break
        if a not in ['u', 'd', 'l', 'r']:
            print("Invalid Instruction! Please try again!")
            continue
        else:
            action = scene1.from_keyboard(a)
        if scene1.is_valid_move(action, posBox, posPlayer):
            posPlayer, posBox = scene1.Move(action, posBox, posPlayer)
            print(posBox)
            print(posPlayer) 
            scene1.PrintMap(posBox, posPlayer, scene1.hole)
        else:
            print("You shall not pass!")

time.sleep(1)



