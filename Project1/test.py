import gamescene
import time 

def testGame():
    scene1 = gamescene.GameScene("demo0.json")
    # 初始化
    posBox = scene1.init_box
    posPlayer = scene1.init_player
    # print(scene1.map)
    # print(scene1.init_player)
    # print(scene1.get_possible_moves())
    scene1.PrintMap(posBox, posPlayer, scene1.hole)
    print("--------------------------------------------------")

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
        # print(scene1.map)
        
        if scene1.isDeadend(posBox): # 陷入死局
            print("Oops! Dead End")
            break
        print("--------------------------------------------------")
    
    print("---------- Congratulations! You Win! ----------")
    print("**************************************************")

def test():
    lista = [["a", 3, 4], ["b", 2, 1], ["c", 5, 2], ["d", 4, 3]]
    listb = [["a", 3, 5], ["b", 2, 1], ["c", 5, 8], ["d", 4, 3]]
    to_be_deleted = []
    i = 0
    for index, a in enumerate(lista):
        if a == listb[index]:
            to_be_deleted.append(index)
    for index in to_be_deleted:
        del lista[index-i]
        i += 1
    print(lista)


testGame()
# start = time.time()
# time.sleep(1)
# end = time.time()
# print(start, end, start-end)

# def x(a, b):
#     return a \
#         if b else None

# print(x('a', 'b'))
# print(x('a', None))


