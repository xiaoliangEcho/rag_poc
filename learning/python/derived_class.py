#!/usr/bin/env python3

class Animal():
    def __init__(self, name='hope'):
        self.name = name
        print(f"My name is {self.name}") 

    def __greet(self):
        print("private greeting!")

    def greet(self):
        print("public greeting!")


class Dog(Animal):
    def __init__(self, name='hope'):
        super().__init__(name)
        print("I am a dog")

a_dog = Dog(name='GoodLuck')
a_dog.greet()
# only call it with updated name
a_dog._Animal__greet()
print(dir(a_dog))
