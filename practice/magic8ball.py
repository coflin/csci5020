#!/usr/bin/python

from random import randint
import time

def main():
    list = ["Yeahhh! For sure!","Nope not happening","Maybe","Concentrate and try again","100%"]
    print(list[randint(0,len(list)-1)])

    a = input("Do you want to try again? Y/N")
    while a == "Y":
        time.sleep(1)
        print(list[randint(0,len(list)-1)])
        a = input("Do you want to try again? Y/N")


if __name__ == "__main__":
    main()

