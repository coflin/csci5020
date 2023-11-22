#!/usr/bin/python

def main():
    fruits = []
    f1 = input("Enter f1: ")
    f2 = input("Enter f2: ")
    f3 = input("Enter f3: ")
    fruits.append(f1)
    fruits.append(f2)
    fruits.append(f3)
    print(sorted(fruits))
    
if __name__ == "__main__":
    main()