#!/usr/bin/python
# This program adds 3 fruits (provided by the user) sorts and prints the list

fruits = []
[fruits.append(input(f"Enter fruit {item+1}: ")) for item in range(3)]
print(f"Sorted list: {sorted(fruits)}")
