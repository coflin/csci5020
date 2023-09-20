#!/usr/bin/python
# Assignment 4: This program checks if a string is a palindrome or not
string = input("Enter a string to check if it's a palindrome: ")
if string == string[::-1]:
    print(f"It's a palindrome")
else:
    print(f"It's not a palindrome")
