#!/usr/bin/python


def addTwoNumbers(l1, l2):
    sum = concat(l1[::-1]) + concat(l2[::-1])
    res = []
    for i in str(sum):
        res.append(int(i))
    print(f"{res}")


def concat(l3):
    num = ""
    for i in l3:
        num = int(str(num) + str(i))
    return num


addTwoNumbers([9, 9, 9, 9, 9], [4, 0])
