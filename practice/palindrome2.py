#!/usr/bin/python

def main():
    string = input("Enter a string: ")
    reverse_string = ""
    for i in range(len(string)):
        reverse_string+=string[-1-i]
    if string == reverse_string:
        print("It is a palindrome!")
    else:
        print("It is not a palindrome!")

if __name__ == "__main__":
    main()