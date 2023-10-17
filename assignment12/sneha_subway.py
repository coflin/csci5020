#!/usr/bin/python

def main():
    class Sub:
        def __init__(self):
            self.breadtype="plain"
            self.sauce="mayonnaise"
            self.topping="no"
        
        def italian_bread(self):
            self.breadtype="italian"
        
        def marinara_sauce(self):
            self.sauce="marinara"

        def olives(self):
            self.topping="olives"
        
        def bake_sub(self):
            print(f"Your sub would be {self.breadtype} bread, {self.sauce} sauce with {self.topping} toppings")

    basicSub = Sub()
    basicSub.bake_sub()

    fancySub = Sub()
    fancySub.italian_bread()
    fancySub.marinara_sauce()
    fancySub.olives()
    fancySub.bake_sub()

if __name__ == "__main__":
    main()