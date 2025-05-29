# Динамическое связывание

В Python, насколько я понимаю, любое связывание -- динамическое вследствие динамической типизации. Тем не менее, представим себе, что типизация статическая. По работе, из недавнего. 
Абстрактный метод предка переопределяется в потомках.
```python
class Command:
    ...
    @abstractmethod
    def do(self, storage: Storage):
        ...

class SimplifyPlineCmd(Command)
    ...
    
    def do(self, storage):
        old_pline = storage[self._pline_id]
        N = len(old_pline)
        new_pline = old_pline[0] + [old_pline[i] if angle(old_pline[i-1, old_pline[i], old_pline[i+1]] < self._max_angle for i in range(1, N-1)] + old_pline[-1]

class MovePlineCmd(Command):
    ...
    def do(self, storage):
        old_pline = storage[self.pline_id]
        new_pline = [pt+self.v for pt in old_pline]
        storage.update(self.pline_id, new_pline)


class Storage:
    def execute_command(self, command: Command):
        # вот тут -- динамическое связывание
        command.do(self)

```
