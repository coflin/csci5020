#!/usr/bin/python
"""
Assignment 12: Dog Park Example. Creates 2 child classes for Daschund and Bulldog
which calls the parent class Dog's speak method.
"""

class Dog:
    species = "Canis familiaris"
    def __init__(self,name,age):
        self.name = name
        self.age = age
        
    def __str__(self):
        return f"{self.name} is {self.age} years old" 
        
    def speak(self, sound):
        print(f"{self.name} says {sound}\n")
        
class Daschund(Dog):
    def speak(self, sound="Arff!"):
        super().speak(sound)
        
class Bulldog(Dog):
    def speak(self,sound="Grrrr!"):
        super().speak(sound)

def main():       
    truffle = Daschund("Truffle",1)
    print(truffle)
    truffle.speak()
    
    psiphon = Bulldog("Psiphon",5)
    print(psiphon)
    psiphon.speak()

if __name__ == "__main__":
     main()