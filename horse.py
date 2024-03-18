# 导入队列库（搜索算法可能需要）
# import queue
from queue import Queue
# 导入随机数库
import random


class ChessBoard:
    def __init__(self, size=8):
        '''
        初始化棋盘
        :param size: 正方形棋盘的边长尺寸，默认为8
        '''
        self.size = size
        # 创建一个二维列表，表示棋盘的状态。
        # 列表的每个元素都是一个空格字符 ' '，表示棋盘上的空位置。
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.start = None # 分别表示马的起始位置
        self.end = None # 和敌方帅的位置
        self.obstacles = [] # 障碍物的位置列表

    def set_start(self, x, y):
        '''
        设置起始点 (马的起始位置)
        :param x: 起始点x坐标
        :param y: 起始点y坐标
        :return: None
        '''
        self.start = (x, y)
        self.board[x][y] = 'S'

    def set_end(self, x, y):
        '''
        设置终止点 (帅的位置)
        :param x: 终止点x坐标
        :param y: 终止点y坐标
        :return: None
        '''
        self.end = (x, y)
        self.board[x][y] = 'E'

    def add_obstacle(self, x, y):
        '''
        添加障碍点
        :param x: 障碍点x坐标
        :param y: 障碍点y坐标
        :return: None
        '''
        self.obstacles.append((x, y))

    def is_valid_move(self, x, y, prev_x, prev_y):
        '''
        判断当前移动是否有效
        :param x: 移动后点的x坐标
        :param y: 移动后点的y坐标
        :param prev_x: 移动前点的x坐标
        :param prev_y: 移动前点的y坐标
        :return: True或False
        '''
        # TODO 1:请在这里补全判断当前移动是否合法的的代码
        if (x < 0 or x >= size) or (y < 0 or y >= size):
            return False
        if self.board[x][y] == 'B': # 目标位置有己方棋子
            return False
        if abs(x - prev_x == 2): # 别马脚情况
            if (self.board[int((x + prev_x) / 2)][y] == 'B' or self.board[int((x + prev_x) / 2)][y] == 'R' or
                self.board[int((x + prev_x) / 2)][prev_y] == 'B' or self.board[int((x + prev_x) / 2)][prev_y] == 'R'):
                return False
        else:
            if (self.board[x][int((y + prev_y) / 2)] == 'B' or self.board[x][int((y + prev_y) / 2)] == 'R' or
                self.board[prev_x][int((y + prev_y) / 2)] == 'B' or self.board[prev_x][int((y + prev_y) / 2)] == 'R'):
                return False
        return True
 

    def is_goal_reached(self, x, y):
        '''
        判断当前是否抵达终点
        :param x: 当前位置的x坐标
        :param y: 当前位置的x坐标
        :return: True或False
        '''
        return (x, y) == self.end

    def get_possible_moves(self, x, y):
        '''
        获取可能的下一步的坐标
        :param x: 当前点的x坐标
        :param y: 当前点的y坐标
        :return: 所有能移动到的有效点坐标的列表
        '''
        possible_moves = [
            (x + 1, y + 2), (x + 2, y + 1),
            (x + 2, y - 1), (x + 1, y - 2),
            (x - 1, y - 2), (x - 2, y - 1),
            (x - 2, y + 1), (x - 1, y + 2)
        ]
        return [(nx, ny) for nx, ny in possible_moves if self.is_valid_move(nx, ny, x, y)]

    def print_board(self):
        '''
        打印当前的棋盘
        :return: None
        '''
        print("+" + "---+" * self.size)
        for row in self.board:
            print("|", end="")
            for cell in row:
                print(f" {cell} |", end="")
            print("\n+" + "---+" * self.size)

    def generate_random_obstacles(self, obstacles_ratio=0.3, seed=0):
        '''
        在棋盘上随机生成一定比例的障碍
        :param obstacles_ratio: 障碍棋子占棋盘位置总数的比例
        :param seed: 随机数种子，控制生成相同的障碍位置
        :return: None
        '''
        num_obstacles = int(obstacles_ratio * self.size * self.size)
        random.seed(seed)
        available_positions = [(x, y) for x in range(self.size) for y in range(self.size)]

        if self.start:
            available_positions.remove(self.start)
        if self.end:
            available_positions.remove(self.end)

        if num_obstacles > len(available_positions):
            print("生成的障碍物数量大于可用位置数量。")
            return

        self.obstacles = random.sample(available_positions, num_obstacles)
        
        for x, y in self.obstacles:
            prob = random.random()
            if prob < 0.5:
                # 红方
                self.board[x][y] = 'R'
            else:
                # 黑方
                self.board[x][y] = 'B'

    def solve(self):
        # TODO 2: 请你在此处补全搜索算法
        node = Horse(list(self.start)) #
        if self.is_goal_reached(node.x, node.y): # 初始马与帅重合？
            return node
        possible_next = self.get_possible_moves(node.x, node.y) # 可能的下一步坐标
        open_queue = Queue()
        closed_set = set()
        open_queue.put(node.position)
        while not open_queue.empty():
            current_state = open_queue.get()
            closed_set.add(tuple(current_state))
            possible_next = self.get_possible_moves(node.x, node.y)
            for next in possible_next:
                # new_state = next                
                if not ((is_in_the_queue(next, open_queue)) or (is_in_set(next, closed_set))): #
                    self.board[node.x][node.y] = ' '
                    self.board[next[0]][next[1]] = 'H'
                    node = Horse(list(next), node)
                    if self.is_goal_reached(node.x, node.y): #
                        return node
                    open_queue.put(node.position)
        return node
                                  

def is_in_the_queue(target, my_queue):
    index = 0
    for i in range(my_queue.qsize()):
        item = my_queue.get()
        if item == target:
            index = index + 1
        my_queue.put(item)
    if index > 0:
        return True
    else:
        return False



def is_in_set(target, my_set):
    for item in my_set:
          if target == item:
            return True
    return False

        
class Horse: # 2024.03.18 added by hry
    def __init__(self, position, parent = None):
        self.position = position # 列表类型
        self.x = position[0]
        self.y = position[1]
        self.parent = parent

    def path(self, start = (0,0)): # 寻找当前马位置到初始位置的路径
        # 它会遍历节点的父节点链，将所有节点添加到一个列表中.
        node, path_back = self, []
        while node.position != list(start):
            path_back.append(node)
            node = node.parent
        path_back.append(node)
        return list(path_back)





# 示例用法
if __name__ == "__main__":
    size = 8
    # 实例化一个大小为size的棋盘
    chessboard = ChessBoard(size=size)
    # 设置初始点为(0,0)
    chessboard.set_start(0, 0)
    # 设置终止点为(n-1,n-1)
    chessboard.set_end(size-1, size-1)
    # 随机生成30%的障碍棋子
    chessboard.generate_random_obstacles(obstacles_ratio=0.3, seed=4)
    # 打印初始棋盘
    print("初始棋盘：")
    chessboard.print_board()
    # 搜索算法求解
    horsenode = chessboard.solve()
    path = list(reversed(horsenode.path()))
    print("path: ")
    for i in path:
        print(list(i.position))
       
