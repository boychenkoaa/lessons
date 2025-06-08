# Задание 11

Для двух классов все хорошо, но увы, не понял, как быть с конструктором NoneClass, если родительских классов будет хотя бы 20...

```python
class General:
	...

class Any(General):
	...
	
class Animal(Any):
	def __init__(self, weight: float):
		self._weight = weight
	
	@property
	def weight(self) -> float:
		return self._weight

class Cat(Animal):
	def meow(self):
		print('meow')

class Dog(Animal):
	def bark(self):
		print('bark')
	
class NoneClass(Cat, Dog):
	pass

none_object = NoneClass(10)
none_object.meow()
none_object.bark()
print(none_object.weight)
```
