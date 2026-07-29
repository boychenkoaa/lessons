from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import Callable, NamedTuple

from pymonad.state import State

"""
Упрощенно имитируем игровой процесс диабло-1 :)

действия:
    - поднять вещь с земли,
    - уложить в инвентарь,
    - переложить из инвентаря в руку и обратно
    - выпить баночку здоровья / маны
    - получить урон в сражении (и умереть если урон больше текущего здоровья)

Для умершего героя меняется состояние на is_alive = False и никакие действия не обсчитываются.
Но делает это неудобно -- вместо Maybe-монады приходится использовать декораторы типа is_alive
"""

# -- базовые классы --

no_change = lambda: State(lambda s: (s, s))


def set_state(new_state):
     return State(lambda _: (new_state, new_state))

# декоратор для действий только с живым персонажем
def only_alive(action):
    def inner(s):
        return no_change() if not s.alive else action(s)
    return inner

# для cond
class PairTuple(NamedTuple):
    pred: bool
    action: Callable

# хочу как в лиспе. Для простоты - без отложенных вычислений.
def cond(*pairs: PairTuple, default: Callable):
    for pair in pairs:
        if pair.pred:
            return pair.action()
    return default()



# -- домен --

# оружие
class Weapon(StrEnum):
    DAGGER = 'dagger'
    SWORD = 'sword'
    LONG_SWORD = 'long_sword'
    AXE = 'axe'
    MACE = 'mace'
    STAFF = 'staff'
    NO_WEAPON = 'NO_WEAPON'

# баночки
class Potion(StrEnum):
    HEALTH = 'health_potion'
    MANA = 'mana_potion'

# состояние игры
# иммутабельно. Методы -- только запросы.
@dataclass(frozen=True)
class GameState:
    MAX_HP = 100
    MAX_MANA = 100
    MAX_SLOTS = 8

    hp: int
    mana: int
    weapon: Weapon
    inventory: dict[str, int] = field(default_factory=dict)
    alive: bool = True

    def __repr__(self):
        if not self.alive:
            return 'DEAD'
        compact = {k: v for k, v in self.inventory.items()}
        return (
            f'hp={self.hp}/{self.MAX_HP}\nmana={self.mana}/{self.MAX_MANA}\nweapon={self.weapon}\ninv={compact}'
        )

    def has_weapon(self, weapon: Weapon) -> bool:
        return self.weapon is weapon or weapon in self.inventory

    def has_item(self, item: str) -> bool:
        return self.inventory.get(item, 0) > 0

    def _total_items(self) -> int:
        return sum(self.inventory.values())

    def add_item(self, item: str, count: int = 1):
        d = self.inventory.copy()
        d[item] = d.get(item, 0) + count
        return replace(self, inventory=d)

    def remove_item(self, item: str, count: int = 1):
        d = self.inventory.copy()
        n = d.get(item, 0) - count
        if n > 0:
            d[item] = n
        else:
            d.pop(item, None)
        return replace(self, inventory=d)



# -- игровая логика --

# действия

def pickup(item):
    """Подобрать оружие с земли. Игнорирует, если инвентарь забит"""
    @only_alive
    def inner(s):
        if s._total_items() >= GameState.MAX_SLOTS:
            return no_change()
        return set_state(s.add_item(item))
    return inner


def drop(item):
    """ Выбросить вещь из инвентаря / из руки """
    @only_alive
    def inner(s):
        return cond(
            PairTuple(item == s.weapon and s.weapon is not Weapon.NO_WEAPON,
                   lambda: set_state(replace(s, weapon=Weapon.NO_WEAPON))),
            PairTuple(s.has_item(item),
                   lambda: set_state(s.remove_item(item))),
            default=no_change,
        )
    return inner


def equip(weapon_name):
    """ Переложить в руку из инвентаря """
    @only_alive
    def inner(s):
        def do_equip():
            s2 = s.remove_item(weapon_name)
            if s.weapon is not Weapon.NO_WEAPON:
                s2 = s2.add_item(s.weapon)
            return set_state(replace(s2, weapon=weapon_name))

        return cond(
            PairTuple(weapon_name is Weapon.NO_WEAPON,              no_change),
            PairTuple(not isinstance(weapon_name, Weapon),          no_change),
            PairTuple(not s.has_item(weapon_name),                  no_change),
            default=do_equip,
        )
    return inner


def drink_health():
    """ пьем баночки здоровья """
    @only_alive
    def inner(s):
        if not s.has_item(Potion.HEALTH):
            return no_change()
        return set_state(replace(s.remove_item(Potion.HEALTH),
            hp=min(s.hp + 30, GameState.MAX_HP)))
    return inner


def drink_mana():
    """ пьем ману """
    @only_alive
    def inner(s):
        if not s.has_item(Potion.MANA):
            return no_change()
        return set_state(replace(s.remove_item(Potion.MANA),
            mana=min(s.mana + 30, GameState.MAX_MANA)))
    return inner


def take_damage(dmg):
    """
        расчет урона при сражении
        если урон больше здоровья, умирает
    """
    @only_alive
    def inner(s):
        new_hp = s.hp - dmg
        if new_hp <= 0:
            return set_state(replace(s, hp=0, alive=False))
        return set_state(replace(s, hp=new_hp))
    return inner


def show():
    """ вывод """
    def inner(s):
        print(s, '\n')
        return no_change()
    return inner


# ── точка входа ──

begin = no_change()

if __name__ == '__main__':
    start = GameState(50, 50, Weapon.DAGGER,
                      {Potion.HEALTH: 2, Potion.MANA: 2, Weapon.LONG_SWORD: 1})

    print('\nТест: перекладываем оружие')
    (begin.bind(show()).bind(equip(Weapon.LONG_SWORD)).bind(show())).run(start)

    print('\nТест: бой + пополняем здоровье здоровья')
    (
        begin.bind(show())
        .bind(drink_health())
        .bind(show())
        .bind(take_damage(40))
        .bind(show())
        .bind(drink_health())
        .bind(show())
    ).run(start)

    print('\nТест: cмерть в бою')
    (
        begin.bind(show())
        .bind(take_damage(60))          # смерть
        .bind(show())
        .bind(drink_health())           # мёртвый не пьёт
        .bind(show())
        .bind(equip(Weapon.LONG_SWORD)) # мёртвый не меняет оружие
        .bind(show())
    ).run(start)
