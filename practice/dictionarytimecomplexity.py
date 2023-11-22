#!/usr/bin/python

import time
dict1 = {"key1":"value1","keys2":"value2","key3":"value3","key4":"value4","key5":"value5"}
dict2 = {"key1":"value1","keys2":"value2"}

tic1 = time.time()
for key,value in dict1.items():
    pass
toc1 = time.time()
print(f"Dictionary of 5 keys/values time is {toc1 - tic1} seconds")

tic2 = time.time()
for key,value in dict2.items():
    pass
toc2 = time.time()
print(f"Dictionary of 2 keys/values time is {toc2 - tic2} seconds\n")
time.sleep(2)

"""
Output: sometimes dict2 is faster than dict1 a few ms and sometimes it's the other way round
sometimes it's the same. Dictionary time complexity = O(N). Let's check for a 100 and 1000 elements.
Might be more clearer.
"""

dict1={}
dict2={}

for i in range(1,1001):
    if i <=100:
        dict1.update({f"key{i}":f"value{i}"})
        dict2.update({f"key{i}":f"value{i}"})
    elif i >= 100:
        dict2.update({f"key{i}":f"value{i}"})

tick1 = time.time()
for key,value in dict1.items():
    pass
tock1 = time.time()
print(f"Dictionary of 100 keys/values time is {tock1 - tick1} seconds")


tick2 = time.time()
for key,value in dict2.items():
    pass
tock2 = time.time()
print(f"Dictionary of 1000 keys/values time is {tock2 - tick2} seconds")