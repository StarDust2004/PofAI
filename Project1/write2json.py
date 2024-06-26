# -*- coding: UTF-8 -*-
"""
@File ：write2json.py
@Author ：Hry
@Date ：2024/04/08 23:50
@Intro: Use this file to write a game scene into a json file
"""
import json

# 准备要写入 JSON 文件的数据
data = {
    "mode": 1, # 箱子与洞口并非一一对应，且箱子推入洞口后还可推出
    "size": [7, 6], # [x,y] [纵向，横向] [从上至下，从左至右]
    "wall": [[0,2], [0,3], [0,4], [0,5], [1,0], [1,1], [1,2], [1,5], [2,0], [2,5],  \
             [3,0], [3,5], [4,0], [4,4], [4,5], [5,0], [5,1], [5,3], [5,4], [6,1], [6,2], [6,3]],
    # "box": [["a",2,2], ["b",3,2], ["c",4,2], ["d",3,3]],
    "box": [["b",3,2], ["a",2,2], ["d",3,3], ["c",4,2]],
    "hole": [["a",3,4], ["c",5,2], ["b",2,1], ["d",4,3]],
    "player": [3,1]
}

data2 = {
    "mode": 0, # 箱子与洞口并非一一对应，且箱子推入洞口后还可推出
    "size": [7, 8], # [x,y]
    "wall": [[0,0], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [1,0], [1,6], [1,7], [2,0], [2,7], \
             [3,0], [3,3], [3,4], [3,7], [4,0], [4,4], [4,7], [5,0], [5,6], [5,7], [6,0], [6,1], \
             [6,2], [6,3], [6,4], [6,5], [6,6]],
    # "box": [["a",2,2], ["b",3,2], ["c",4,2], ["d",3,3]],
    "hole": [['e',4,3], ['b',5,1], ['a',5,2], ['c',5,3], ['d',5,5]],
    "box": [['a',2,2], ['b',3,1], ['c',3,2], ['d',3,5], ['e',4,2]],
    "player": [4,1]
}

level2 = {
    "mode": 0, # 无对应关系
    "size": [11, 18], 
    "hole": [["a", 6, 15], ["b", 6, 16], ["c", 7, 15], ["d", 7, 16], ["e", 8, 15], ["f", 8, 16]], 
    "box": [["a", 2, 5], ["b", 3, 7], ["c", 4, 5], ["d", 4, 8], ["e", 7, 2], ["f", 7, 5]], 
    "wall": [[0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13], \
             [0, 14], [0, 15], [0, 16], [0, 17], [1, 4], [1, 8], [1, 9], [1, 10], [1, 11], \
             [1, 12], [1, 13], [1, 14], [1, 15], [1, 16], [1, 17], [2, 4], [2, 8], [2, 9], \
             [2, 10], [2, 11], [2, 12], [2, 13], [2, 14], [2, 15], [2, 16], [2, 17], [3, 2], \
             [3, 3], [3, 4], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14], [3, 15],\
             [3, 16], [3, 17], [4, 2], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [4, 15], \
             [4, 16], [4, 17], [5, 0], [5, 1], [5, 2], [5, 4], [5, 6], [5, 7], [5, 8], [5, 10],\
             [5, 12], [5, 13], [5, 14], [5, 15], [5, 16], [5, 17], [6, 0], [6, 4], [6, 6], [6, 7],\
             [6, 8], [6, 10], [6, 11], [6, 12], [6, 17], [7, 0], [7, 17], [8, 0], [8, 1], [8, 2], \
             [8, 3], [8, 4], [8, 6], [8, 7], [8, 8], [8, 9], [8, 11], [8, 12], [8, 17], [9, 4], \
             [9, 11], [9, 12], [9, 13], [9, 14], [9, 15], [9, 16], [9, 17], [10, 4], [10, 5], \
             [10, 6], [10, 7], [10, 8], [10, 9], [10, 10], [10, 11], [10, 16], [10, 17]], 
    "player": [7, 12]
}

mode0_2 = {
    "mode": 0,
    "size": [9, 9], 
    "hole": [["a", 2, 1], ["b", 3, 5], ["c", 4, 1], ["d", 5, 4], ["e", 6, 3], ["g", 6, 6], ["h", 7, 4]], 
    "wall": [[0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [1, 0], [1, 1], [1, 2], [1, 6], [1, 7], [1, 8], [2, 0], [2, 6], [2, 7], [2, 8], [3, 0], [3, 1], [3, 2], [3, 6], [3, 7], [3, 8], [4, 0], [4, 2], [4, 3], [4, 6], [4, 7], [4, 8], [5, 0], [5, 2], [5, 6], [5, 7], [5, 8], [6, 0], [6, 7], [6, 8], [7, 0], [7, 7], [7, 8], [8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 7]], 
    "box": [["a", 2, 3], ["b", 3, 4], ["c", 4, 4], ["d", 6, 1], ["f", 6, 3], ["g", 6, 4], ["h", 6, 5]], 
    "player": [2, 2]
}

mode1_2_no = {
    "mode": 1,
    "size": [9, 9], 
    "hole": [["a", 2, 1], ["b", 3, 5], ["c", 4, 1], ["d", 5, 4], ["e", 6, 3], ["g", 6, 6], ["h", 7, 4]], 
    "wall": [[0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [1, 0], [1, 1], [1, 2], [1, 6], [1, 7], [1, 8], [2, 0], [2, 6], [2, 7], [2, 8], [3, 0], [3, 1], [3, 2], [3, 6], [3, 7], [3, 8], [4, 0], [4, 2], [4, 3], [4, 6], [4, 7], [4, 8], [5, 0], [5, 2], [5, 6], [5, 7], [5, 8], [6, 0], [6, 7], [6, 8], [7, 0], [7, 7], [7, 8], [8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 7]], 
    "box": [["a", 2, 3], ["b", 3, 4], ["c", 4, 4], ["d", 6, 1], ["f", 6, 3], ["g", 6, 4], ["h", 6, 5]], 
    "player": [2, 2]
}

mode0_3 = {
    "mode": 0,
    "size": [7, 10],
    "hole": [["a", 4, 2], ["b", 4, 3], ["c", 5, 2], ["d", 5, 3]],
    "wall": [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [1, 0], [1, 1], [1, 7], [1, 8], [1, 9], [2, 0], [2, 1], [2, 3], [2, 4], [2, 5], [2, 9], [3, 0], [3, 9], [4, 0], [4, 4], [4, 9], [5, 0], [5, 1], [5, 4], [5, 9], [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8], [6, 9]], 
    "box": [["a", 2, 2], ["b", 3, 4], ["c", 3, 7], ["d", 4, 6]],
    "player": [3, 1]
}

mode1_3 = {
    "mode": 1,
    "size": [7, 10],
    "hole": [["a", 5, 2], ["b", 5, 3], ["c", 4, 2], ["d", 4, 3]],
    "wall": [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [1, 0], [1, 1], [1, 7], [1, 8], [1, 9], [2, 0], [2, 1], [2, 3], [2, 4], [2, 5], [2, 9], [3, 0], [3, 9], [4, 0], [4, 4], [4, 9], [5, 0], [5, 1], [5, 4], [5, 9], [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8], [6, 9]], 
    "box": [["a", 2, 2], ["b", 3, 4], ["c", 3, 7], ["d", 4, 6]],
    "player": [3, 1]
}

demo0 = {
    "size": [9, 8],\
    "mode": 0,\
    "player": [2,2],\
    "box": [['a',2,3], ['b',3,4],['c',4,4],['d',6,1],['e',6,3],['f',6,4],['g',6,5]],\
    "hole":[['a',2,1], ['b',3,5],['c',4,1],['d',5,4],['e',6,3],['f',6,6],['g',7,4]],\
    "wall":[[0,2],[0,3],[0,4],[0,5],[0,6],[1,0],[1,1],[1,2],[1,6],[2,0],[2,6],[3,0],[3,1],\
            [3,2],[3,6],[4,0],[4,2],[4,3],[4,6],[5,0],[5,2],[5,6],[5,7],[6,0],[6,7],[7,0],\
            [7,7],[8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[8,6],[8,7]]
}

demo1 = {
    "size": [9, 8],\
    "mode": 1,\
    "player": [2,2],\
    "box": [['a',2,3], ['b',3,4],['c',4,4],['d',6,1],['e',6,3],['f',6,4],['g',6,5]],\
    "hole":[['a',2,1], ['b',3,5],['d',4,1],['c',5,4],['e',6,3],['g',6,6],['f',7,4]],\
    "wall":[[0,2],[0,3],[0,4],[0,5],[0,6],[1,0],[1,1],[1,2],[1,6],[2,0],[2,6],[3,0],[3,1],\
            [3,2],[3,6],[4,0],[4,2],[4,3],[4,6],[5,0],[5,2],[5,6],[5,7],[6,0],[6,7],[7,0],\
            [7,7],[8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[8,6],[8,7]]
}

mode0_4 = {
    'mode': 0,
    'size': [6,6],
    'player': [2,4],
    'box': [['a',2,2], ['b',3,4]],
    'hole': [['a',1,1], ['b',4,4]],
    'wall': [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[1,0],[1,5],[2,0],[2,1],[2,3],[2,5],\
             [3,1],[3,5],[4,1],[4,2],[4,3],[4,5],[5,3],[5,4],[5,5]]
}
mode1_4 = {
    'mode': 1,
    'size': [6,6],
    'player': [2,4],
    'box': [['a',2,2], ['b',3,4]],
    'hole': [['b',1,1], ['a',4,4]],
    'wall': [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[1,0],[1,5],[2,0],[2,1],[2,3],[2,5],\
             [3,1],[3,5],[4,1],[4,2],[4,3],[4,5],[5,3],[5,4],[5,5]]
}

mode0_5 = {
    'mode': 0,
    'size': [8,6],
    'player': [6,2],
    'box': [['a',3,3],['b',4,3],['c',5,2],['d',5,3]],
    'hole': [['a',1,3],['b',2,1],['c',4,4],['d',5,2]],
    'wall': [[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,4],[2,0],[2,4],[3,0],[3,1],[3,4],[3,5],\
             [4,0],[4,5],[5,0],[5,5],[6,0],[6,5],[7,0],[7,1],[7,2],[7,3],[7,4],[7,5]]
}
mode1_5 = {
    'mode': 1,
    'size': [8,6],
    'player': [6,2],
    'box': [['a',3,3],['b',4,3],['c',5,2],['d',5,3]],
    'hole': [['a',1,3],['c',2,1],['b',4,4],['d',5,2]],
    'wall': [[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,4],[2,0],[2,4],[3,0],[3,1],[3,4],[3,5],\
             [4,0],[4,5],[5,0],[5,5],[6,0],[6,5],[7,0],[7,1],[7,2],[7,3],[7,4],[7,5]]
}

mode0_0 = {
    "mode": 0,
    "size": [11, 18], 
    "hole": [["a", 6, 15], ["b", 6, 16], ["c", 7, 15], ["d", 7, 16], ["e", 8, 15], ["f", 8, 16]], 
    "box": [["a", 2, 5], ["b", 3, 7], ["c", 4, 5], ["d", 4, 8], ["e", 7, 2], ["f", 7, 5]], 
    "player": [7, 12],
    "wall": [[0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13], [0, 14], [0, 15], [0, 16], [0, 17], [1, 4], [1, 8], [1, 9], [1, 10], [1, 11], [1, 12], [1, 13], [1, 14], [1, 15], [1, 16], [1, 17], [2, 4], [2, 8], [2, 9], [2, 10], [2, 11], [2, 12], [2, 13], [2, 14], [2, 15], [2, 16], [2, 17], [3, 2], [3, 3], [3, 4], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14], [3, 15], [3, 16], [3, 17], [4, 2], [4, 10], [4, 11], [4, 12], [4, 13], [4, 14], [4, 15], [4, 16], [4, 17], [5, 0], [5, 1], [5, 2], [5, 4], [5, 6], [5, 7], [5, 8], [5, 10], [5, 12], [5, 13], [5, 14], [5, 15], [5, 16], [5, 17], [6, 0], [6, 4], [6, 6], [6, 7], [6, 8], [6, 10], [6, 11], [6, 12], [6, 17], [7, 0], [7, 17], [8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 6], [8, 7], [8, 8], [8, 9], [8, 11], [8, 12], [8, 17], [9, 4], [9, 11], [9, 12], [9, 13], [9, 14], [9, 15], [9, 16], [9, 17], [10, 4], [10, 5], [10, 6], [10, 7], [10, 8], [10, 9], [10, 10], [10, 11], [10, 16], [10, 17]]
    }

mode0_6 = {
    "mode": 0,
    "size": [10, 14], 
    "player": [4, 7],
    "hole": [["a", 1, 1], ["b", 1, 2], ["c", 2, 1], ["d", 2, 2], ["e", 3, 1], ["f", 3, 2], ["g", 4, 1], ["h", 4, 2], ["i", 5, 1], ["j", 5, 2]], 
    "box": [["a", 2, 7], ["b", 2, 10], ["c", 3, 6], ["d", 5, 10], ["e", 6, 9], ["f", 6, 11], ["g", 7, 4], ["h", 7, 7], ["i", 7, 9], ["j", 7, 11]], 
    "wall": [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13], [1, 0], [1, 5], [1, 11], [1, 12], [1, 13], [2, 0], [2, 5], [2, 13], [3, 0], [3, 5], [3, 7], [3, 8], [3, 9], [3, 10], [3, 13], [4, 0], [4, 9], [4, 10], [4, 13], [5, 0], [5, 5], [5, 7], [5, 12], [5, 13], [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 7], [6, 8], [6, 13], [7, 2], [7, 13], [8, 2], [8, 7], [8, 13], [9, 2], [9, 3], [9, 4], [9, 5], [9, 6], [9, 7], [9, 8], [9, 9], [9, 10], [9, 11], [9, 12], [9, 13]],
    }
 

# 写入文件的数据可能是乱序的，所以在GameScene的读取函数里需要处理乱序问题
def write2json(data, filename):
    # 打开文件并将数据写入文件
    # filename = 'mode0_2.json'
    with open(filename, 'w') as f:
        # json.dump(data, f, indent=2)  # 使用 indent 参数指定缩进，可选
        json.dump(data, f)

    print(f"JSON 数据已写入文件 '{filename}'")

write2json(mode0_6, "jsonMaps/mode0_6.json")
# write2json(mode0_5, "jsonMaps/mode0_5.json")
# write2json(mode1_4, "jsonMaps/mode1_4.json")
# write2json(mode1_5, "jsonMaps/mode1_5.json")