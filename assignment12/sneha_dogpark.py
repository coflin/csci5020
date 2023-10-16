#!/usr/bin/python

class Dog:
    species = "Toy Poodle"
    def __init__(self,name,age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return(f"My name is {self.name} and my age is {self.age}")

tommy = Dog("tommy",1)
tommy.specy = "Adult Poodle"
print(tommy.specy)
print(tommy.name)