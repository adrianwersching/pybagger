from bag_status import BagStatus
from fruitbagger import Fruitbagger

if __name__ == "__main__":
    auth_key = input("Enter authorization key\n")
    bagger = Fruitbagger(auth_key)

    bagger.open_session()
    bagger.open_bag()
    fruit, status = bagger.get_fruit()
    sum = 0

    while status == BagStatus.OK:
        bagger.bag_fruit(fruit)
        sum += fruit.weight
        if sum >= 1000:
            print("Sum: " + str(sum))
            bagger.close_bag()
            bagger.open_bag()
            sum = 0
        fruit, status = bagger.get_fruit()

    bagger.close_session()
