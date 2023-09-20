#!/usr/bin/python
# Assignment 4: This program checks if a string is a palindrome or not
string = input("Enter a string to check if it's a palindrome: ")
string = string.replace(" ", "")
reversestring = ""
for index in range(len(string)):
    reversestring += string[len(string) - 1 - index]
if string == reversestring:
    print(f"It's a palindrome")
else:
    print(f"It's not a palindrome")
