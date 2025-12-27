"""
Одна из моих мини-абстракций (не новая, но...)
Field -- иммутабельное поле.
Одна из ключевых частей самопального pydantic (оригинальный pydantic меня смущает обилием возможностей).

Оно всегда валидно и всегда иммутабельно (метод with_value возвращает None при невалидном значении -- этакая попытка присваивания)
Создан для удобства передачи данных, общения с GUI -- этакий "связующий" класс между бизнес-логикой и пользовательским интерфейсом.

Field не абстрактный, у него есть реализация, но самая общая.
На практике она неудобная и переопределяется в наследниках: DictField, TupleField, ListField, FilenameField, ...

Если к DictField добавить аннотации полей, то получится Model из MVC и MVVM
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Dict, Generic, Self

from core.validators import (
    ArrayValidator,
    ArrayValidatorTVar,
    CartesianValidator,
    CartesianValidatorTVar,
    DictValidator,
    EnumValidator,
    FileNameExtensionValidator,
    SimpleListTVar,
    SimpleListValueT,
    SimpleTVar,
    SimpleValidatorT,
    SimpleValueT,
    TableTVar,
    TableValidator,
    TableValueT,
    TupleTVar,
    TupleValidator,
    TupleValueT,
    TVar,
    Validator,
    ValidatorT,
)

"""
Общие принципы для полей.

1. Все поля -- иммутабельные.
Ни один метод не изменяет состояние.

2. В целом можно обойтись одним только Field с кастомным валидатором и обновлять по значению.
Наследники от Field со специфичными методами (типа TableField например с возможностью "изменить" ячейку) -- для удобства.
Например при привязке к событиям того же UI.

3. Все "методы-команды" -- возвращают или новый объект или None, при неуспехе (невалидное значение на входе).
Исключений не бросают.

4. Методы-запросы могут бросить исключение (типа index out of range или подобного) при невалидных параметрах.

5. Сериализация и десериализация -- по дефолту через JSON, но при желании можно переопределить и настроить свою.
"Мягкая" сериализация (типа в список/кортеж/таблицу строк и из нее) -- полностью кастомная.
Опять же, она только для удобства.
"""


# чистую строку зеркалирует, остальное экспортирует в джсон
# для избежания двойных кавычек вокруг одиночной строки -- они совсем не нужны
# кортежи и составные типы со строками не пострадают от этого
def to_str_smart(primitive: Any):
    if isinstance(primitive, str):
        return primitive
    return json.dumps(primitive)


# если не смог распарсить джсоном -- зеркалирует строку
def from_str_smart(s: str) -> Any:
    ans = s
    try:
        ans = json.loads(s)
    except:
        pass
    return ans


class Field:
    def __init__(self, validator: ValidatorT, value: Any = None):
        ...
    
    def clone(self) -> "Field":
        ...
    
    def validator(self) -> ValidatorT:
        ...
    
    def is_valid(self) -> bool:
        ...
    
    def value(self) -> Any:
        ...
    
    def to_str(self) -> str:
        ...
    
    def with_value(self, value: Any) -> "Field":
        ...
    
    def from_str(self, value_str: str) -> "Field":
        ...
    
    def __repr__(self) -> str:
        ...

class EnumField(Field):
    def __init__(self, enum_type: type[Enum], value: Any = None):
        ...
    
    def values(self) -> list[str]:
        ...

class TupleField(Field):
    def __init__(self, components: tuple[ValidatorT, ...], value: Any = None):
        ...
    
    def to_str_tuple(self) -> tuple[str, ...]:
        ...
    
    def from_str_tuple(self, value_str_tuple: tuple[str, ...]) -> "TupleField":
        ...
    
    def is_valid_item(self, index: int, value: Any) -> bool:
        ...
    
    def update_field(self, index: int, value: Any) -> "TupleField":
        ...
    
    def update_field_from_str(self, index: int, value_str: str) -> "TupleField":
        ...

class ListSimpleField(Field):
    def __init__(self, item_validator: ValidatorT, value: Any = None):
        ...
    
    def is_valid_item(self, value: Any) -> bool:
        ...
    
    def get_item(self, index: int) -> Any:
        ...
    
    def to_str_list(self) -> list[str]:
        ...
    
    def from_str_list(self, value_str_list: list[str]) -> "ListSimpleField":
        ...
    
    def update_item(self, index: int, value: Any) -> "ListSimpleField":
        ...
    
    def insert(self, index: int, value: Any) -> "ListSimpleField":
        ...
    
    def pop_head(self) -> tuple[Any, "ListSimpleField"]:
        ...
    
    def pop_tail(self) -> tuple[Any, "ListSimpleField"]:
        ...
    
    def pop(self, index: int) -> tuple[Any, "ListSimpleField"]:
        ...
    
    def insert_to_head(self, value: Any) -> "ListSimpleField":
        ...
    
    def insert_to_tail(self, value: Any) -> "ListSimpleField":
        ...

class TableField(Field):
    def __init__(self, columns: tuple[ValidatorT, ...], value: Any = None):
        ...
    
    def get_row(self, index: int) -> tuple[Any, ...]:
        ...
    
    def get_cell(self, row_index: int, column_index: int) -> Any:
        ...
    
    def to_str_table(self) -> list[list[str]]:
        ...
    
    def is_valid_row(self, row: tuple[Any, ...]) -> bool:
        ...
    
    def is_valid_cell(self, row_index: int, column_index: int, value: Any) -> bool:
        ...
    
    def from_str_table(self, value_str_table: list[list[str]]) -> "TableField":
        ...
    
    def update_row(self, row_index: int, row: tuple[Any, ...]) -> "TableField":
        ...
    
    def update_cell(self, row_index: int, column_index: int, value: Any) -> "TableField":
        ...
    
    def update_cell_from_str(self, row_index: int, column_index: int, value_str: str) -> "TableField":
        ...
    
    def update_row_from_str_tuple(self, row_index: int, value_str_tuple: tuple[str, ...]) -> "TableField":
        ...
    
    def insert(self, row_index: int, row: tuple[Any, ...]) -> "TableField":
        ...
    
    def insert_to_head(self, row: tuple[Any, ...]) -> "TableField":
        ...
    
    def insert_to_tail(self, row: tuple[Any, ...]) -> "TableField":
        ...
    
    def remove(self, row_index: int) -> "TableField":
        ...
    
    def remove_from_head(self) -> "TableField":
        ...
    
    def remove_from_tail(self) -> "TableField":
        ...
    
    def clear(self) -> "TableField":
        ...

class DictField(Field):
    def __init__(self, fields: dict[str, ValidatorT], value: Any = None):
        ...
    
    def field_names(self) -> list[str]:
        ...
    
    def update_item(self, field_name: str, value: Any) -> "DictField":
        ...
    
    def concat(self, other: "DictField") -> "DictField":
        ...
    
    def value(self) -> dict[str, Any]:
        ...

class FileNameOpenField(Field):
    def __init__(self, extensions: list[str], value: Any = None):
        ...
    
    def extensions(self) -> list[str]:
        ...

class FileNameSaveField(Field):
    def __init__(self, extensions: list[str], value: Any = None):
        ...
    
    def extensions(self) -> list[str]:
        ...
