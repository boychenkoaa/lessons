from copy import deepcopy
from typing import TypeVar, Generic, Type

"""
StackSounder.sound_stack()  вызывается ковариантно
внутри него идет полиморфное обращение к animal.sound()
"""

T_co = TypeVar('T_co', covariant=True)
class Stack(Generic[T_co]):
    def __init__(self) -> None:
        # Create an empty list with items of type T
        self.items: list[T_co] = []

    def push(self, item: T_co) -> None:
        self.items.append(item)

    def pop(self) -> T_co:
        return self.items.pop()

    def empty(self) -> bool:
        return not self.items
    
    def __repr__(self) -> str:
        return f"Stack({self.items})"


class Animal():
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Animal({self.name})"
    
    def __str__(self) -> str:
        return self.name

    def sound(self):
        return "???"

class Cat(Animal):
    def sound(self):
        return 'meow'

class Dog(Animal):
    def sound(self):
        return 'bark'

class Duck(Animal):
    def sound(self):
        return 'quack'

class SoundNoise:
    def noise(self):
        return '????'

class xSoundNoise:
    def noise(self):
        return 'xxxxx'

class ySoundNoise:
    def noise(self):
        return 'yyyyy'

T_noise = TypeVar('T_noise', bound=SoundNoise, covariant=True)
T_animal_co = TypeVar('T_animal_co', bound=Animal, covariant=True)

class StackSounder(Generic[T_noise]):
    def __init__(self, cls: Type[T_noise]):
        self.noiz = cls()

    def sound_stack(self, s: Stack[T_animal_co]):
        print(self.noiz.noise())
        while not s.empty():
            animal = s.pop() 
            # animal.sound - полимрфный вызов            
            print(animal.name, ': ', animal.sound())
        print(self.noiz.noise())

animal_stack = Stack[Animal]()
dog_stack = Stack[Dog]()

animal_stack.push(Dog('Fido'))
animal_stack.push(Cat('Whiskers'))
animal_stack.push(Duck('Donald'))
animal_stack2 = deepcopy(animal_stack)

dog_stack.push(Dog('Rover'))
dog_stack.push(Dog('Spot'))
dog_stack.push(Dog('Bublik'))

sounder_x = StackSounder[xSoundNoise](xSoundNoise)
sounder_y = StackSounder[ySoundNoise](ySoundNoise)

# ковариантный вызов
sounder_x.sound_stack(animal_stack)
sounder_y.sound_stack(dog_stack)
sounder_x.sound_stack(animal_stack2)
