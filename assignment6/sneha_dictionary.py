#!/usr/bin/python
"""
Assignment 6: Converts two lists to one dictionary where list1 contains all the keys
and list2 contains all values.
"""

#Convert any two given lists to a dictionary
def listtodict(list1,list2):
    dictionary={}
    for key,value in zip(list1,list2): dictionary[key]=value 
    #Print the keys, values and entire dictionary
    print(f'Dictionary keys:\n {dictionary.keys()}\n')
    print(f'Dictionary values: \n {dictionary.values()}\n')
    print(f'Entire dictionary:\n {dictionary}\n')

def main():
    countries=["USA","India","Norway"]
    capitals=["Washington D.C.","New Delhi","Oslo"]
    listtodict(countries,capitals)

if __name__ == "__main__":
    main()