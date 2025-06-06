# Задача 10.
Прямой возможности нет, но есть декоратор `@final` из `typing`

Пример: контейнер с доступом по айди. Его можно расширять (например, искать по значению, либо реализовывать еще какие-то запросы), либо специализировать. 
Но переопределять базовые операции со словарем нежелательно. 
Если мы хотим вместо словаря использовать, скажем, дерево, можно выделить интерфейс, унаследоваться от него и там уже вводить свои операции.

```python
from typing import final

class DictIDContainer:
	def __init__(self):
		self._di = {}
		self._last_id = 0

	@final
	def __update_id(self):
		self._last_id += 1

	@final
	def __getitem__(self, id_: int):
		return self._di[item]

	@final
	def remove(self, id_: int):
		self._di.pop(id_)

	@final
	def add_item(self, new_value):
		self._update_id()
		self._di[self._last_id] = new_value
	
```
