# Решение задания 4

IDStorageExec (контейнер с айди) и Command связаны через двойную диспетчеризацию
```python
# storage.py

# немного упрощен
class IDStorage:
	def __init__(self):
		self._last_id = 0
		self._di = {}
		
	def __getitem__(self, item):
		return self._di.get(item)

	def add(self, new_object):
		self._di[self._last_id] = new_object
		self._last_id += 1

	def remove(self, id_: int):
		self._di.remove(id)

	@property
	def last_id(self):
		return self._last_id

class IDStorageExec(IDStorage):
	def exec_command(self, command: Command):
		command.do(self)

# commands.py
class Command():
	def do(self, storage: IDStorage):
		...

```

- `commands.py` открыт для изменений (наследуемся от `Command` и добавляем логику), 
- `Storage` закрыт -- любые изменения внутри повлекут очень неприятные последствия, хотя бы для тех же `Command` -- это базовый модуль, от него зависят остальные
