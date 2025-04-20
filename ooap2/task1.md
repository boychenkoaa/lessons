## Задание 1 (полиморфизм, наследование, композиция)

- Класс главного окна MainWindow наследуется от `QMainWindow` (стандартные методы, либо не переопределяются, либо дополняют родительские)
- Композиция: QTreeView и QLabel и прочие элементы вложены в Tab2D(композиция)
- Полиморфизм: paretn = self во всех конструкторах - ожидается QWidget, по факту используются все его наследники. Динамическая типизация позволяет это делать даже более свободно, чем нужно.
```python
class TabMain(QWidget):
    def __init__(self, parent=None):
	    super().__init__(self, parent)
        self._btn_next = QButton(self, "Next")
        ...

class Tab2D(QWidget):
    def __init__(self):
        super().__init__(self, parent)
        self._btn_next = QButton(self, "Next")
        self._tree_view = QTreeView(parent = self)
        self._status_label = QLabel(parent = self)
        ...

class MainWindow(QMainWindow):
    def __init__(self):
        self._tab_main = TabMain(self)
        self._tab_2d = Tab2D(self)
        self._tab_widget.addTab("Main", self._tab_widget)
        self._tab_widget.addTab("2D", self._tab_2d )
        self._menu = QMenu(self)
```
