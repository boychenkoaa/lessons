'''
1. метод публичен в родительском классе А и публичен в его потомке B;
2. метод публичен в родительском классе А и скрыт в его потомке B;
3. метод скрыт в родительском классе А и публичен в его потомке B;
4. метод скрыт в родительском классе А и скрыт в его потомке B.
'''

'''
2 и 3 в Python в чистом виде нет, реализуем максимально близко:
2 через вызов raise AttributeError
3 через переименование

1 и 4 определяются только в родителе, потомок унаследует их автоматически
'''

from typing import override


class Parent:
    def method1(self):
        print('parent-1')
        
    def _method4(self):
        print('parent-4')
        
    def _method3(self):
        print('parent-3')
        
    def method2(self):
        print('parent-2')
    
class Child(Parent):
    def method3(self):
        super().method3()
        print('child-3')
        
    @override
    def method2(self):
        raise AttributeError
