# -*- coding: UTF-8 -*-
"""
@File : node.py
@Author ：Hry
@Date ：2024/04/16 16:29
@Intro: to create a class for node in the A* search tree
@Modify: 
"""

from gamescene import GameScene

# 与游戏布局和位置相关的属性不应当被改变 eg: self.posBox/self.posPlayer不应修改
class Node():
    def __init__(self, posBox, posPlayer, parent = None, path_cost = 0, action = None):
        self.posBox = posBox # 游戏过程中，箱子位置列表，对当前node而言不应当改变
        self.posPlayer = posPlayer # 角色位置（用列表表示的一个二元组合），对当前node而言不应当改变 eg:[1,1] 
        self.path_cost = path_cost # 路径代价，g(n)
        # self.depth = depth # 深度
        self.action = action # 从父节点到本节点采取的行动，['u', 'd', 'l', 'r'], 用于生成child_node
        self.parent = parent
        self.depth = 0 # 深度，此处其实认为从初始状态至此的路径代价g(n) = 深度
        # “还未解决的箱子列表”
        # 在mode==1中，用于记录还没有到达指定洞口的箱子，其他箱子已经消失，所以从box列表中删除了
        # 在mode==0中，始终等于self.posBox
        self.pendingBox = self.posBox # 修改了GameScene中的代码，应该不需要了 2024/04/117 00:25
        if self.parent: # 如果有父节点
            self.depth = self.parent.depth + 1 # 深度 = 父节点深度 + 1

    """ 
    # 根据给定参数，生成新的子节点
    def child_node(self, posBox, posPlayer, action, problem: GameScene):
        a_child_node = Node(posBox, posPlayer, self, self.depth + 1, action) # 生成子节点

        if problem.mode == 1: # 箱子推入对应的洞口后，会消失！要把消失的箱子删掉去
            delete_num = [] # 用来记录要删除的箱子的序号
            i = 0
            for index, box in enumerate(a_child_node.pendingBox):
                if box == problem.hole[index]:
                    delete_num.append(index)
            for index in delete_num:
                del a_child_node.pendingBox[index-i] # 删除子节点中那些已经到位，应该消失的箱子
                i += 1            

        return a_child_node 
    """

    # 根据给定参数，生成新的子节点
    def child_node(self, posBox, posPlayer, action):
        a_child_node = Node(posBox, posPlayer, self, self.depth + 1, action) # 生成子节点
        return a_child_node 
    
    # 根据父节点->当前节点的链表，得到从初始节点到当前节点的路径
    def path(self):
        """ path_back = [self]
        node = self.parent
        while node.parent != None:
            path_back.append(node)
        path_back.append(node) """
        node = self
        path_back = []
        while node != None:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    
    # 打印初始节点到当前节点的路径上经过的所有行动, 单个行动用['u', 'd', 'l', 'r']之一表示
    def path_action_print(self):
        path = self.path
        for node in path:
            print(node.action, end = ' -> ')

    # 计算评价函数值f(n) = g(n) + h(n)，代表节点的优先级, 越小越优先
    def Prior(self, problem: GameScene):
        hn = problem.Heuristic_func(self.posBox) # 启发函数值, 使用posBox计算
        # 不使用pendingBox的原因是，pendingBox已经删除了到达预期点的箱子，会对应不上
        # g(n): path_cost
        return self.path_cost + hn
    
    # 返回一个表示节点的可读字符串。在调试和输出日志时有用，显示了节点的玩家位置、箱子位置和路径代价
    def __repr__(self):
        return "<Node {}{}(g={})>".format(self.posPlayer, self.posBox, self.path_cost)

    # 定义了节点之间的小于比较运算。它用于优先队列中的节点排序，以便按照路径代价g(n)从小到大的顺序取出节点
    def __lt__(self, other):
        return self.path_cost < other.path_cost

    # 判等函数，定义为：仅当两个节点的玩家位置和箱子位置全部一致，才认为二者相等
    def __eq__(self, other):
        return (self.posBox == other.posBox and self.posPlayer == other.posPlayer)
    
    # def hash_value(self): # 返回了状态的哈希值，以便将状态用作字典的键，以提高搜索效率。
    #     "return hashable value of state"
    #     return self.posBox.tobytes() # 需要是numpy才行？






