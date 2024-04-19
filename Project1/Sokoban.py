"""
# File       : UI.py
# Time       ：2024/4/18 8:39
# Author     ：Hry
# Description：to set ui for the game and start the game
"""
# 包含界面设计和最终进行游戏的代码
# 是最后被调用的.py文件

import os, sys

# 资源文件目录访问
def source_path(relative_path):
    # 是否被打包成可执行文件（frozen）
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else: # 未被打包，则将当前工作目录设为基础路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 修改当前工作目录，使得资源文件可以被正确访问
cd = source_path('') # 当前目录
os.chdir(cd) # 将当前工作目录更改为本文件当前所在目录

from collections import deque
import pygame, sys, os, time
from pygame.locals import *
from search import AStarSearch
from gamescene import GameScene
import time
import random

# W <-> list/array.y(从左往右), H <-> list/array.x(从上往下)
# W <-> pygame.x(从左往右), H <-> pygame.y(从上往下)
# W/H没有方向之分

# 按钮
class Button:
    def __init__(self, ButtonUpImage, ButtonDownImage, pos):
        # 按钮未按下时的图像（鼠标不在按钮范围内）
        self.ButtonUp = pygame.image.load(ButtonUpImage).convert_alpha()
        # 按钮被按下时的图像（鼠标在按钮范围内）
        self.ButtonDown = pygame.image.load(ButtonDownImage).convert_alpha()
        # 按钮中心在窗口中的位置
        self.pos = pos

    # 检查鼠标是否在按钮图片范围内
    def Mouse_In_Button(self):
        playerx, playery = pygame.mouse.get_pos() # 获取鼠标位置[x,y]
        x, y = self.pos # 按钮图片中心位置 [x,y]
        w, h = self.ButtonUp.get_size() # 图片的宽度、高度
        return (x - w/2 < playerx < x + w/2) and (y - h/2 < playery < y + h/2)

    # 在窗口中显示按钮
    def show(self, screen):
        x, y = self.pos # 按钮图片中心位置 [x,y]
        w, h = self.ButtonUp.get_size() # 图片的宽度、高度
        # 根据鼠标位置变换显示样式, 输入左上角坐标
        if self.Mouse_In_Button(): # 被按下
            screen.blit(self.ButtonDown, (x - w / 2, y - h / 2))
        else: # 没有被按下
            screen.blit(self.ButtonUp, (x - w / 2, y - h / 2))


# 显示游戏主界面 --- 界面1
# param screen: Pygame 屏幕对象，用于显示界面
# param interface: 图片数据, 主界面图片
# param startGame: 开始游戏按钮,Button
# param introduction: 游戏说明按钮，Button
# return: int
# return 1: 开始游戏
# return 2: 游戏说明
def ShowGameInterface(screen, interface, startGame: Button, introduction: Button ):
    for event in pygame.event.get():
        if event.type == QUIT: # 关闭程序
            pygame.quit()
            sys.exit() # 退出，关闭
        elif event.type == MOUSEBUTTONDOWN: # 按下鼠标
            if startGame.Mouse_In_Button(): # 点击了“开始游戏”
                return 1
            elif introduction.Mouse_In_Button(): # 点击了“游戏说明”
                return 2
    
    screen.blit(interface, (0, 0)) # 占满整个屏幕的interface（主界面背景）
    startGame.show(screen) # 显示“开始游戏”按钮
    introduction.show(screen) # 显示“游戏说明”按钮
    return 0 # 没有点击按钮 

    

# 选择游玩模式界面 --- 界面2
# 选择玩家模式/AI模式/返回
# param screen：Pygame 屏幕对象，用于显示界面。
# param interface：游玩模式选择界面的背景图像。
# param player: 玩家模式按钮
# param AI: AI模式按钮
# param return_to_prev：返回上一个界面的按钮。Button
# return: int
# return 1: 玩家模式
# return 2: AI模式
# return 3: 返回上一个界面（界面1、主界面）
def SelectGameMode(screen, interface, player: Button, AI: Button, return_to_prev: Button):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if player.Mouse_In_Button(): # 鼠标点击“玩家模式”
                return 1
            elif AI.Mouse_In_Button(): # 鼠标点击“AI模式”
                return 2
            elif return_to_prev.Mouse_In_Button(): # 鼠标点击“返回”
                return 3
        else:
            pass

    screen.blit(interface, (0,0)) # 绘制背景
    player.show(screen) # 显示“玩家模式”按钮
    AI.show(screen) # “AI模式”按钮
    return_to_prev.show(screen) # “返回”按钮
    return 0 


# 选择关卡类型界面 --- 界面3
# 选择关卡中箱子与洞口的对应关系, 在selectGameMode后调用
# mode = 0: 箱子与洞口之间无对应关系，箱子入洞后仍然可以被推出 -> return 1
# mode = 1: 箱子与洞口一一对应，箱子进入对应洞口后直接消失 -> return 2
# param screen：Pygame 屏幕对象，用于显示界面。
# param interface：关卡选择界面的背景图像。
# param level_select：包含不同关卡选择选项按钮的字典。{Button, Button, ...}
# param return_to_prev：返回上一个界面的按钮。Button
# return: int 用于选择不同的关卡类型 1/2/3:mode0 / mode1 / 返回上一级（界面2）
# 通过迭代 Pygame 事件来处理用户交互。
# 如果用户点击了特定的关卡选择按钮或返回上一个界面的按钮，函数会返回相应的代码，指示用户的选择。
# 在处理完事件之后，函数会将背景图像和所有关卡选择按钮绘制到屏幕上。
# 最后，如果用户在此帧中没有采取任何操作，则返回 0。
def SelectLevelMode(screen, interface, level_select, return_to_prev: Button):
    for event in pygame.event.get():
        if event.type == QUIT: # 关闭程序
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if level_select['mode0'].Mouse_In_Button(): # 点击'mode0'按钮
                return 1
            elif level_select['mode1'].Mouse_In_Button(): # 点击'mode1'按钮
                return 2
            elif return_to_prev.Mouse_In_Button(): # 点击“返回”按钮
                return 3
            else:
                pass
    # 绘制背景图片
    screen.blit(interface, (0, 0))
    level_select['mode0'].show(screen) # 'Mode 0' button
    level_select['mode1'].show(screen) # 'Mode 1' button

    return_to_prev.show(screen) # “返回”按钮
    return 0



# 成功结束界面 --- 界面5？
# 展示一个成功的图片，打印通关用的步数，显示“返回-选择关卡”按钮
# param screen: 游戏窗口对象，用于在其上显示通关界面。
# param interface: 背景图片，作为通关界面的背景。
# param returnToChoose: 返回选关的按钮对象，点击该按钮可以返回选关界面。
# param count: 通关所用的步数，将在通关界面中显示
# return 0 # 返回0，表示通关界面显示完毕，没有触发返回选关的行为
# return 1 # 返回值设为1，表示需要返回选关界面 -> 界面3
def ShowGameWin(screen, interface, return_to_prev: Button, count: int):
    for event in pygame.event.get():
        if event.type == QUIT: # 关闭程序
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if return_to_prev.Mouse_In_Button(): # 点击“返回”按钮
                return 1 # 返回值设为1，表示需要返回选关界面 -> 界面3
    # 绘制背景图片
    screen.blit(interface, (0, 0))
    # 打印一个通关所用的步数
    font = pygame.font.Font('font/FreeSansBold.ttf', 30)
    text = font.render(f"TOTAL STEPS:{count}", True, (255, 0, 0), interface.get_at((10, 10)))
    textRect = text.get_rect()  # 获得显示对象的 rect区域大小
    textRect.center = (300, 450)  # 设置文字位置
    screen.blit(text, textRect)
    # 显示“返回选关”按钮
    return_to_prev.show(screen)
    return 0 # 返回0，表示通关界面显示完毕，没有触发返回选关的行为


# 失败结束界面（玩家模式-进入死局）
def ShowGameDeadEnd(screen, interface, return_to_prev: Button, count: int):
    for event in pygame.event.get():
        if event.type == QUIT: # 关闭程序
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if return_to_prev.Mouse_In_Button(): # 点击“返回”按钮
                return 1 # 返回值设为1，表示需要返回选关界面 -> 界面3
    # 绘制背景图片
    screen.blit(interface, (0, 0)) # 输了
    # 打印一个通关所用的步数
    font = pygame.font.Font('font/FreeSansBold.ttf', 30)
    text = font.render("Oops! Dead End!", True, (255, 0, 0), interface.get_at((10, 10)))
    textRect = text.get_rect()  # 获得显示对象的 rect区域大小
    textRect.center = (300, 450)  # 设置提示语句位置
    screen.blit(text, textRect)
    # 显示“返回选关”按钮
    return_to_prev.show(screen)
    return 0 # 返回0，表示通关界面显示完毕，没有触发返回选关的行为


# 玩家模式
# param clock: Pygame 的时钟对象，用于控制游戏循环的速度。
# param screen: 游戏窗口对象，用于在其上绘制游戏界面。
# param skin: 游戏背景色。图片数据
# param pics: 包含游戏元素图片的字典，包括空地、player、箱子box、墙、洞口等。Dict:{png,png,...}
# param level_json: 可选参数，表示当前游戏的关卡。.json
# param info: 可选参数，表示游戏信息。.json.data
# return: int(0/1/2), int(steps)
# 如果玩家选择(Esp)退出游戏，则返回0和步数计数器;
# 如果游戏胜利，返回1和步数计数器；
# # 待添加的功能：如果局面陷入了死局(DeadEnd)，则返回2和步数计数器
def PlayerMode(clock, screen, skin, pics, level_json = None, info = None):
    # 初始化游戏场景
    if level_json != None: 
        # 如果传入了关卡信息.json文件，则从对应的 JSON 文件中加载地图数据
        skb = GameScene(level_json) # short for sokoban game
    else: # 如果没有传入关卡信息.json文件，则根据给定的信息初始化地图
        skb = GameScene(info = info)
    posBox = skb.init_box # 箱子列表
    posPlayer = skb.init_player # 玩家位置
    # 绘制游戏窗口
    # screen.fill(skin.get_at((0, 0))) # 将游戏窗口填充为背景色
    screen.blit(skin, (0,0)) # 将游戏窗口的背景图设置为skin
    # 绘制游戏初始界面，包括玩家和箱子的初始位置
    skb.DisplayScene(posBox, posPlayer, screen, pics['blank'], pics['player'], \
                     pics['box'], pics['wall'], pics['hole'], pics['boxinhole'])
    step_count = 0 # 计数器（玩家步数）

    # 利用双端队列deque来维护历史操作队列
    dq = deque([]) # 历史操作
    # 游戏进程主循环，不断监听事件并更新游戏状态
    while True:
        clock.tick(60) # 控制游戏循环的速度,以每秒 60 帧的速度运行
        action = None # 行动
        for event in pygame.event.get(): # 监听事件，包括退出事件QUIT和按键事件KEYDOWN
            if event.type == QUIT: # 关闭程序
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN: # 按键
                if event.key == K_ESCAPE: # Escape键，退出循环
                    return 0, step_count
                
                # "上下左右"按键操作，通过GameScene.from_keyboard给出行动指令
                # 画面更新，调用Move函数进行移动改变布局
                # 然后把这一步对象（包括由移动方向和move()函数返回值构成的操作记录元组）放进deque内保存
                # 绘制改变布局后的新的界面
                if event.key == K_LEFT: # 左 l
                    action = skb.from_keyboard('l')
                elif event.key == K_RIGHT: # 右 r
                    action = skb.from_keyboard('r')
                elif event.key == K_UP: # 上 u
                    action = skb.from_keyboard('u')
                elif event.key == K_DOWN: # 下 d
                    action = skb.from_keyboard('d')
                elif event.key == K_BACKSPACE: # 回退一步
                    # 如果队列不为空
                    if len(dq) > 0:
                        # 取出当前队尾的对象（操作记录元组）
                        op = dq.pop()
                        posBox, posPlayer = op[1], op[2]
                        step_count -= 1 # 移动步数--
        
        # 判断当前操作是否合法，如果合法则更新玩家和箱子的位置，并更新步数计数器
        if action != None and skb.is_valid_move(action, posBox, posPlayer):
            # print(posBox) # debug
            dq.append([action, posBox, posPlayer]) # 加入历史操作
            posPlayer, posBox = skb.Move(action, posBox, posPlayer)
            step_count += 1
            # print(posBox,'   ', skb.hole)  # debug 
        skb.DisplayScene(posBox, posPlayer, screen, pics['blank'], pics['player'], \
                         pics['box'], pics['wall'], pics['hole'], pics['boxinhole'])
        
        # 显示当前步数：
        font = pygame.font.Font('font/FreeSansBold.ttf', 20)
        text = font.render(f"STEPS:{step_count}", True, (255, 0, 0), skin.get_at((0, 0)))
        textRect = text.get_rect()   # 获得显示对象的 rect区域大小
        textRect.center = (300, 50)  # 设置位置
        screen.blit(text, textRect)  # 显示当前步数
        pygame.display.update()
        # 如果按下Backblank按键，则进行回退操作, act = None, 并且显示上一步操作后的游戏界面
        # 如果当前队列长度大于50（即存放的操作记录元组数超过50条），则取出队首的对象（即丢弃最早的一条记录），以保持当前队列长度在50以内
        if len(dq) > 50:
            dq.popleft()
        # 如果isSuccess为真，则过关
        if skb.isSuccess(posBox):
            # print("player Mode: Success") # debug
            pygame.time.delay(1000) # 暂停一秒
            clock.tick(60)
            pygame.display.update()
            return 1, step_count
        # 加一条对死局的判断？类似于：
        if skb.isDeadend(posBox): # 陷入死局
            # print("player mode: Oops! Dead End") # 修改为在游戏界面上显示 # debug
            pygame.time.delay(1000) # 暂停一秒
            clock.tick(60)
            pygame.display.update()
            return 2, step_count # -> 用于在接下来调用GameDeadEnd(),同时也显示步数？
        pygame.display.update()



# AI模式
# param clock: 游戏时钟对象，用于控制游戏帧率。
# param screen: 游戏窗口对象，用于显示游戏画面。
# param skin: 游戏窗口的背景颜色。图片数据
# param pics: 包含游戏中用到的所有图片资源。{png,png,...}
# param level_json: 可选参数，表示要加载的关卡文件的级别。如果为 None，则使用 info。.json
# param info: 可选参数，表示游戏的其他信息 .json.data
# return:
# 第一个返回值: 表示游戏是否胜利，0 表示游戏退出，1 表示游戏胜利。(2表示找不到解)
# 第二个返回值: 表示游戏使用的步数。
def AIMode(clock, screen, skin, pics, level_json = None, info = None):
    # 初始化游戏场景
    if level_json != None:
        skb = GameScene(level_json)
    else:
        skb = GameScene(info=info)
    posBox = skb.init_box # 箱子列表
    posPlayer = skb.init_player # 玩家位置
    # 绘制游戏窗口
    # screen.fill(skin.get_at((0, 0))) # 将游戏窗口填充为背景色
    screen.blit(skin, (0,0)) # 将游戏窗口的背景图设置为skin
    # 绘制游戏初始界面，包括玩家和箱子的初始位置
    skb.DisplayScene(posBox, posPlayer, screen, pics['blank'], pics['player'], \
                     pics['box'], pics['wall'], pics['hole'], pics['boxinhole'])
    
    # 显示提示语句
    font = pygame.font.Font('font/FreeSansBold.ttf', 20)
    text = font.render(f"Waiting for AI to Search!", True, (255, 0, 0), skin.get_at((0, 0)))
    textRect = text.get_rect()  # 获得显示对象的 rect区域大小
    textRect.center = (300, 50)  # 设置位置
    screen.blit(text, textRect)  # 显示等待 AI 搜索的提示文字
    pygame.display.update()
    start_time = time.time() # 开始时间
    res = AStarSearch(skb) # A* 搜索算法找到最优路径
    

    # 找不到搜索路径，会return None，res = None
    # 是不是应该显示:
    if res is None: # 没有找到路径
        font = pygame.font.Font('font/FreeSansBold.ttf', 20)
        text = font.render(f"Can't Find A Solution!", True, (255, 0, 0), skin.get_at((0, 0)))
        textRect = text.get_rect()  # 获得显示对象的 rect区域大小
        textRect.center = (300, 300)  # 设置位置
        screen.blit(text, textRect)  # 显示失败提示
        pygame.display.update()
        pygame.time.delay(1000) # 暂停一秒
        return 2, 0
    # font = pygame.font.Font('font/FreeSansBold.ttf', 20)
    # text = font.render(f"Can't Find A Solution!", True, (255, 0, 0), skin.get_at((0, 0)))
    # textRect = text.get_rect()  # 获得显示对象的 rect区域大小
    # textRect.center = (400, 400)  # 设置位置
    # screen.blit(text, textRect)  # 显示失败提示
    # pygame.display.update()
    # return 2, 0


    end_time = time.time() # 结束时间
    time_cost = end_time - start_time # 用时
    print(f'time cost:{time_cost}s') # report
    print("movement path:", end = ' ')
    actions = res.path_action_print() # 打印路径
    # final_node.pathprint()
    # print(final_node)
    print(f'\ndepth/steps:{res.path_cost}') # 深度/步数

    # 找到了路径
    path = res.path()

    step_count = 0
    # 游戏进程主循环: 不断更新游戏画面，直到完成整个路径的展示
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT: # 直接关闭程序
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 用户按下了Escape按键，则退出游戏进程循环
                if event.key == K_ESCAPE:
                    return 0, step_count

        pygame.display.update()
        node = path[step_count]
        skb.DisplayScene(node.posBox, node.posPlayer, screen, pics["blank"], pics["player"], pics["box"], pics["wall"], pics["hole"], pics["boxinhole"])
        font = pygame.font.Font('font/FreeSansBold.ttf', 20)
        text = font.render(f"STEPS:{step_count},TOTAL STEPS:{len(path)-1}", True, (255, 0, 0), skin.get_at((0, 0)))
        textRect = text.get_rect()  # 获得显示对象的 rect区域大小
        textRect.center = (300, 50)  # 设置位置
        screen.blit(text, textRect)
        time.sleep(0.5)
        pygame.display.update()
        step_count+=1
        if(step_count>=len(path)):
            break

    pygame.display.update()
    pygame.time.delay(1000) # 暂停一秒
    return 1,len(path)-1



# 最终调用的函数:进行游戏的主程序
def showgame():
    # 初始化pygame
    pygame.init()
    # 加载各项游戏资源（异常处理）
    try:
        gameicon = pygame.image.load('pictures/basic_pics/BoxIcon.png')# 设置游戏图标
        pygame.display.set_icon(gameicon) # 展示游戏图标
        screen = pygame.display.set_mode((600,600)) # 设置主界面大小
        
        # 加载游戏所需的资源，如图标、按钮图片、游戏界面背景等
        button_start = Button('pictures/button_pics/start_button_up.png', 'pictures/button_pics/start_button_down.png', (300, 400)) # “开始游戏”按钮
        button_intro = Button('pictures/button_pics/intro_button_up.png', 'pictures/button_pics/intro_button_down.png', (300, 500))  # “游戏说明”按钮

        # 玩家模式按钮
        player_button = Button('pictures/button_pics/player_button_up.png', 'pictures/button_pics/player_button_down.png', (300, 300))
        # AI模式按钮
        AI_button = Button('pictures/button_pics/ai_button_up.png', 'pictures/button_pics/ai_button_down.png', (300, 400))

        # 进入关卡类型选择(mode0/mode1)的一堆按钮
        mode0 = Button('pictures/button_pics/mode0_button_up.png', 'pictures/button_pics/mode0_button_down.png', (300,300)) # mode0, 无对应关系
        mode1 = Button('pictures/button_pics/mode1_button_up.png', 'pictures/button_pics/mode1_button_down.png', (300,400)) # mode1, 有对应关系

        # 关卡类型选择->放进一个字典里
        level_select = {}
        level_select["mode0"] = mode0
        level_select["mode1"] = mode1

        button_ret_start = Button('pictures/button_pics/return_button_up.png', 'pictures/button_pics/return_button_down.png', (300,500)) # “返回主界面”按钮,界面2->1
        button_ret_mode = Button('pictures/button_pics/return_button_up.png', 'pictures/button_pics/return_button_down.png', (300,500)) # “返回选择游玩模式”按钮,界面3->2
        button_ret_select = Button('pictures/button_pics/return_button_up.png', 'pictures/button_pics/return_button_down.png', (300,500)) # “返回选关”按钮,界面5->3

        interface = pygame.image.load("pictures/basic_pics/main1.png") # 主界面
        introduction = pygame.image.load("pictures/basic_pics/introduction.png")  # 游戏说明界面图片
        play_mode = pygame.image.load("pictures/basic_pics/play_mode.png") # 选择游玩模式图片
        level_mode = pygame.image.load("pictures/basic_pics/level_mode.png") # 选择关卡界面图片
        chapterpass = pygame.image.load("pictures/basic_pics/youwin.png") # 通关提示界面图片
        chapterfail = pygame.image.load("pictures/basic_pics/youlose.png") # 陷入死局界面图片

        # blank = pygame.image.load("pictures/30p30/blank.png") # 空地
        # player = pygame.image.load("pictures/30p30/ghost.png") # 玩家/角色
        # box = pygame.image.load("pictures/30p30/box.png") # 箱子
        # wall = pygame.image.load("pictures/30p30/wall.png") # 墙
        # hole = pygame.image.load("pictures/30p30/hole.png") # 洞口
        # boxinhole = pygame.image.load("pictures/30p30/box_in_hole.png")  # 箱子在洞 # 注：人在洞里就直接把洞挡住
        blank = pygame.image.load("pictures/40p40/blank.png") # 空地
        player = pygame.image.load("pictures/40p40/cat.png") # 玩家/角色
        box = pygame.image.load("pictures/40p40/box.png") # 箱子
        wall = pygame.image.load("pictures/40p40/wall3.png") # 墙
        hole = pygame.image.load("pictures/40p40/hole.png") # 洞口
        boxinhole = pygame.image.load("pictures/40p40/box_in_hole.png")  # 箱子在洞 # 注：人在洞里就直接把洞挡住
        # skin = pygame.image.load("pictures/30p30/space.png") # 背景色
        # skin = pygame.image.load('pictures/basic_pics/skin7.png') # 背景图
        skin = pygame.image.load('pictures/basic_pics/skin5_1.png') # 背景图

        pics = {} # 选择图片 -> 字典
        pics["interface"],pics["introduction"],pics["play_mode"],pics["level_mode"],pics["chapterpass"],pics["chapterfail"] = interface, introduction, play_mode, level_mode, chapterpass, chapterfail
        pics["blank"],pics["player"],pics["box"],pics["wall"],pics["hole"],pics["boxinhole"] = blank, player, box, wall, hole,boxinhole
    
    except pygame.error as msg:
        raise(SystemExit(msg))
    
    mode0_json = ['jsonMaps/mode0_1.json', 'jsonMaps/mode0_2.json', 'jsonMaps/mode0_3.json']
    mode1_json = ['jsonMaps/mode1_1.json', 'jsonMaps/mode1_2.json', 'jsonMaps/mode1_3.json']
    
    pygame.display.set_caption('Project1: Sokoban Player and Solver') # 设置游戏界面标题
    clock = pygame.time.Clock() # 设置游戏进行过程中的定时器
    # 按住某个键每隔interval(50)毫秒产生一个KEYDOWN事件，delay(200)就是多少毫秒后才开始触发这个事件
    pygame.key.set_repeat(200,50)

    # 游戏主循环
    while True:
        # 设置游戏绘制的最大帧率
        flag = ShowGameInterface(screen, interface, button_start, button_intro) # flag记录了用户在主界面上点击的是哪个按钮
        # 如果点击 开始游戏 : -> player_or_ai(choose: player_mode) -> choose: level_mode(选择关卡类型0/1)
        if flag == 1: # 选择游戏模式（player / AI)
            while True:
                # 选择 player/AI 模式 / 返回主界面
                mode = SelectGameMode(screen,play_mode,player_button, AI_button, button_ret_start)
                if mode == -1 or mode == 0: # 没反应 # mode绘制了背景图片后会返回0
                    pygame.display.update()
                    continue
                if mode == 3: # 按下返回按钮，退出，又回到主界面等待下一个输入
                    break
                if mode == 1: # 玩家模式 player -> 选择关卡类型choose level_mode
                    while True:
                        # 选择关卡类型 level_mode, 3是返回上一界面（return_to_mode选择player_or_ai的界面)
                        match = SelectLevelMode(screen, level_mode, level_select, button_ret_mode)
                        if match == -1 or match == 0:  # 没反应
                            pygame.display.update()
                            continue
                        if match == 3:  # 退出,回到上一级界面
                            break
                        if match == 1:  # mode0
                            random_num = random.randint(0, len(mode0_json) - 1) # 生成范围内的随机数
                            # debug
                            # win, steps = PlayerMode(clock, screen, skin, pics, mode0_json[random_num])
                            # win, steps = PlayerMode(clock, screen, skin, pics, 'jsonMaps/mode0_3.json')
                            # win, steps = PlayerMode(clock, screen, skin, pics, 'jsonMaps/demo0.json')
                            win,steps = PlayerMode(clock, screen, skin, pics, 'jsonMaps/mode0_6.json')
                            if win == 1: # 获胜
                                while True:
                                    ret = ShowGameWin(screen, chapterpass, button_ret_select, steps)
                                    pygame.display.update()
                                    if ret:
                                        break
                                pygame.display.update()
                            elif win == 2: # 死局
                                while True:
                                    ret = ShowGameDeadEnd(screen, chapterfail, button_ret_select, steps)
                                    pygame.display.update()
                                    if ret:
                                        break
                                pygame.display.update()
                            else:
                                pass
                                
                        if match == 2: # mode1
                            random_num = random.randint(0, len(mode1_json) - 1) # 生成范围内的随机数
                            win, steps = PlayerMode(clock, screen, skin, pics, mode1_json[random_num])
                            if win == 1: # 获胜
                                while True:
                                    ret = ShowGameWin(screen, chapterpass, button_ret_select, steps)
                                    pygame.display.update()
                                    if ret:
                                        break
                                pygame.display.update()
                            elif win == 2: # 死局
                                while True:
                                    ret = ShowGameDeadEnd(screen, chapterfail, button_ret_select, steps)
                                    pygame.display.update()
                                    if ret:
                                        break
                                pygame.display.update()
                            else:
                                pass
                        pygame.display.update()

                if mode == 2: # AI模式
                    while True:
                        # 选择关卡类型 level_mode, 3是返回上一界面（return_to_mode选择player_or_ai的界面)
                        match = SelectLevelMode(screen, level_mode, level_select, button_ret_mode)
                        if match == -1 or match == 0:  # 没反应
                            pygame.display.update()
                            continue
                        if match == 3:  # 退出
                            break
                        if match == 1:  # mode0
                            # debug
                            random_num = random.randint(0, len(mode0_json) - 1) # 生成范围内的随机数
                            # win, steps = AIMode(clock, screen, skin, pics, mode0_json[random_num])
                            # win, steps = AIMode(clock, screen, skin, pics, "jsonMaps/mode0_3.json") # debug
                            # win, steps = AIMode(clock, screen, skin, pics, 'jsonMaps/demo0.json')
                            win, steps = AIMode(clock, screen, skin, pics, 'jsonMaps/mode0_6.json')
                            if win == 1: # 获胜
                                while True:
                                    ret = ShowGameWin(screen, chapterpass, button_ret_select, steps)
                                    pygame.display.update()
                                    if ret:
                                        break
                                pygame.display.update()
                            elif win == 2: # 死局
                                while True:
                                    ret = ShowGameDeadEnd(screen, chapterfail, button_ret_select, steps)
                                    pygame.display.update()
                                    if ret:
                                        break
                                pygame.display.update()
                            else:
                                pass

                        if match == 2:  # mode1
                            # debug
                            random_num = random.randint(0, len(mode1_json) - 1) # 生成范围内的随机数
                            # win, steps = AIMode(clock, screen, skin, pics, mode1_json[random_num])
                            # win, steps = AIMode(clock, screen, skin, pics, "jsonMaps/mode1_3.json")
                            # win, steps = AIMode(clock, screen, skin, pics, "jsonMaps/demo1.json")
                            win, steps = AIMode(clock, screen, skin, pics, "jsonMaps/mode1_3.json")

                            if win == 1: # 获胜
                                while True:
                                    ret = ShowGameWin(screen, chapterpass, button_ret_select, steps)
                                    pygame.display.update()
                                    if ret:
                                        break
                                pygame.display.update()
                            elif win == 2: # 死局
                                while True:
                                    ret = ShowGameDeadEnd(screen, chapterfail, button_ret_select, steps)
                                    pygame.display.update()
                                    if ret:
                                        break
                                pygame.display.update()
                            else:
                                pass
                        pygame.display.update()
                pygame.display.update()

        # 如果点击了“游戏说明”按钮
        elif flag == 2: # 显示游戏说明页面，等待用户按下Esc键返回主界面。
            clock.tick(60)
            retGameInterface = False
            while True:
                for event in pygame.event.get(): # 等待用户按下Esc键返回主界面
                    if event.type == QUIT: # 直接关闭页面
                        pygame.quit()
                        sys.exit() # 退出游戏程序
                    elif event.type == KEYDOWN: # 按下Esc键
                        if event.key == K_ESCAPE:
                            retGameInterface = True # 返回主界面
                            break
                screen.blit(introduction, (0,0))
                pygame.display.update()
                if retGameInterface == True:
                    break # 停止显示gametips, 返回主界面
        pygame.display.update()




if __name__ == '__main__':
    showgame()


