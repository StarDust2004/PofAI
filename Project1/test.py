import gamescene

scene1 = gamescene.GameScene("demo1.json")
# print(scene1.map)
# print(scene1.init_player)
# print(scene1.get_possible_moves())
scene1.PrintMap(scene1.posBox, scene1.posPlayer, scene1.hole)
print("--------------------------------------------------")
# scene1.Move([-1,0,'u'])
# print(scene1.posBox)
# print(scene1.posPlayer)
# print(scene1.get_possible_moves())
# scene1.Move([0,1,'r'])
# print(scene1.posBox)
# print(scene1.posPlayer)
while scene1.isSuccess() != True:
    a = input("choose a direction:")
    if a == 'q':
        break
    if a not in ['u', 'd', 'l', 'r']:
        print("Invalid Instruction! Please try again!")
        continue
    else:
        action = scene1.from_keyboard(a)
    if scene1.is_valid_move(action):
        scene1.Move(action)
        print(scene1.posBox)
        print(scene1.posPlayer) 
        scene1.PrintMap(scene1.posBox, scene1.posPlayer, scene1.hole)
    else:
        print("You shall not pass!")
    # print(scene1.map)
    
    if scene1.isDeadend(scene1.posBox): # 陷入死局
        print("Oops! Dead End")
        break
    print("--------------------------------------------------")

