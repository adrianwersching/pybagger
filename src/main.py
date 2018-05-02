import sys
from operator import attrgetter

from bag_status import BagStatus
from fruitbagger import Fruitbagger


def get_best_fruit(lookahead, sum):
    best_fruit = None
    best_diff = sys.maxsize

    # find fruit with that gets sum as close to 1000 as possible
    for fruit in lookahead:
        diff = (sum + fruit.weight) - 1000
        if 0 <= diff < best_diff:
            best_fruit = fruit
            best_diff = diff

    # otherwise return max fruit or random fruit
    if best_fruit is not None:
        return best_fruit
    else:
        if sum < 500:
            return max(lookahead, key=attrgetter("weight"))
    return lookahead[0]


if __name__ == "__main__":
    auth_key = input("Enter authorization key\n")
    bagger = Fruitbagger(auth_key)
    bagger.open_session()
    bagger.open_bag()

    sum = 0
    lookahead = []
    last_status = None
    for i in range(0, 4):
        fruit, status = bagger.get_fruit()
        lookahead.append(fruit)
        last_status = status

    while last_status == BagStatus.OK:
        best_fruit = get_best_fruit(lookahead, sum)
        bagger.bag_fruit(best_fruit)
        lookahead.remove(best_fruit)
        sum += best_fruit.weight

        if sum >= 1000:
            print("Sum: " + str(sum))
            bagger.close_bag()
            bagger.open_bag()
            sum = 0
        fruit, last_status = bagger.get_fruit()
        lookahead.append(fruit)
    bagger.close_session()
