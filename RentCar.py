import random

def Rent(x, total_hours):
    car_A, car_B = 100, 100 # A/B开始时各有100辆车
    customer_A, customer_B = 0, 0 # A/B开始都各有0个顾客
    rent_A, rent_B = 0, 0 # A/B开始都各租出去了0辆车
    ind_A, ind_B = 0, 0 # 指示当前循环中A、B各自是否租了车

    for i in range(total_hours):
        if random.uniform(0, 1) < 0.3: # A地有人租车
            customer_A += 1 # A地顾客++
            if car_A > 0:
                car_A -= 1 # 租出去一辆车
                # car_B += 1 # 下一个循环B地会多一辆车
                ind_A = 1
                rent_A += 1 # 累计租出去的车数量++
        if random.uniform(0, 1) < 0.5: # B地有人租车
            customer_B += 1 # B地顾客++
            if car_B > 0:
                car_B -= 1 # 租出去一辆车
                # car_A += 1 # 下一个循环A地会多一辆车
                ind_B = 1
                rent_B += 1 # 累计租出去的车数量++
        if i % x == 0:
            temp = car_A >> 1
            car_A -= temp
            car_B += temp
        car_A += ind_B
        car_B += ind_A # 下一个循环B地会多 零或者一 辆车
        ind_A = 0
        ind_B = 0

    pos = 1 - rent_B / customer_B
    # print("概率是：{:.2f}".format(pos))
    print("B地租不到车的概率是:", pos)

if __name__ == '__main__':
    x = int(input("每x个小时进行一次车辆转移: x = "))
    total_hours = int(input("一共运行多少小时呢？"))
    Rent(x, total_hours)
