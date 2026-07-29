from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import Callable, NamedTuple

from pymonad.state import State

"""
Упрощенно имитируем игровой процесс диабло-1 :)

Лог событий накапливается в value State-монады, а не в GameState.
Каждое действие получает накопленный лог через bind и дописывает своё событие.
"""

# -- базовые классы --

no_change = lambda: State(lambda s: ((), s))


def only_alive(action):
    """Мёртв — лог и состояние не меняются. Жив — выполняем действие."""
    def inner(log):
        return State(lambda s:
            (log, s) if not s.alive
            else action(log).run(s)
        )
    return inner


# для cond
class PairTuple(NamedTuple):
    pred: bool
    action: Callable


def cond(*pairs: PairTuple, default: Callable):
    for pair in pairs:
        if pair.pred:
            return pair.action()
    return default()



# -- домен --

class Weapon(StrEnum):
    DAGGER = 'dagger'
    SWORD = 'sword'
    LONG_SWORD = 'long_sword'
    AXE = 'axe'
    MACE = 'mace'
    STAFF = 'staff'
    NO_WEAPON = 'NO_WEAPON'


class Potion(StrEnum):
    HEALTH = 'health_potion'
    MANA = 'mana_potion'


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

def pickup(item):
    """Подобрать оружие с земли. Игнорирует, если инвентарь забит"""
    @only_alive
    def inner(log):
        return State(lambda s: (
            log + (f'инвентарь полон, {item} не подобран',),
            s,
        ) if s._total_items() >= GameState.MAX_SLOTS else (
            log + (f'подобран {item}',),
            s.add_item(item),
        ))
    return inner


def drop(item):
    """ Выбросить вещь из инвентаря / из руки """
    @only_alive
    def inner(log):
        return State(lambda s: cond(
            PairTuple(item == s.weapon and s.weapon is not Weapon.NO_WEAPON,
                   lambda: (log + (f'выброшен {item} (из руки)',),
                            replace(s, weapon=Weapon.NO_WEAPON))),
            PairTuple(s.has_item(item),
                   lambda: (log + (f'выброшен {item}',),
                            s.remove_item(item))),
            default=lambda: (log + (f'нечего выбрасывать: {item}',), s),
        ))
    return inner


def equip(weapon_name):
    """ Переложить в руку из инвентаря """
    @only_alive
    def inner(log):
        return State(lambda s: cond(
            PairTuple(weapon_name is Weapon.NO_WEAPON,
                   lambda: (log + ('нельзя экипировать пустую руку',), s)),
            PairTuple(not isinstance(weapon_name, Weapon),
                   lambda: (log + (f'неизвестное оружие: {weapon_name}',), s)),
            PairTuple(not s.has_item(weapon_name),
                   lambda: (log + (f'нет в инвентаре: {weapon_name}',), s)),
            default=lambda: _do_equip(log, s, weapon_name),
        ))
    return inner


def _do_equip(log, s, weapon_name):
    s2 = s.remove_item(weapon_name)
    old = s.weapon
    if old is not Weapon.NO_WEAPON:
        s2 = s2.add_item(old)
    event = f'экипирован {weapon_name}'
    if old is not Weapon.NO_WEAPON:
        event += f' (старый {old} → инвентарь)'
    return (log + (event,), replace(s2, weapon=weapon_name))


def drink_health():
    """ пьем баночки здоровья """
    @only_alive
    def inner(log):
        return State(lambda s: (
            log + ('нет баночек здоровья',), s,
        ) if not s.has_item(Potion.HEALTH) else (
            log + (f'+{min(s.hp + 30, GameState.MAX_HP) - s.hp} hp',),
            replace(s.remove_item(Potion.HEALTH),
                    hp=min(s.hp + 30, GameState.MAX_HP)),
        ))
    return inner


def drink_mana():
    """ пьем ману """
    @only_alive
    def inner(log):
        return State(lambda s: (
            log + ('нет баночек маны',), s,
        ) if not s.has_item(Potion.MANA) else (
            log + (f'+{min(s.mana + 30, GameState.MAX_MANA) - s.mana} mana',),
            replace(s.remove_item(Potion.MANA),
                    mana=min(s.mana + 30, GameState.MAX_MANA)),
        ))
    return inner


def take_damage(dmg):
    """ расчет урона. Если урон > hp — смерть """
    @only_alive
    def inner(log):
        return State(lambda s: (
            log + (f'-{s.hp} hp 💀 умер',),
            replace(s, hp=0, alive=False),
        ) if s.hp - dmg <= 0 else (
            log + (f'-{dmg} hp',),
            replace(s, hp=s.hp - dmg),
        ))
    return inner


def show():
    """ вывод состояния на экран (побочный эффект, лог не меняет) """
    def inner(log):
        return State(lambda s: (
            print(s, '\n') or log,
            s,
        ))
    return inner


def collect_log():
    """ финальный шаг: лог из value наружу (уже и так там, просто заглушка) """
    def inner(log):
        return State(lambda s: (log, s))
    return inner


def print_log(log):
    """Вывод лога на печать."""
    print('Лог:')
    for i, event in enumerate(log, 1):
        print(f'  {i}. {event}')


# ── точка входа ──

begin = no_change()

if __name__ == '__main__':
    start = GameState(50, 50, Weapon.DAGGER,
                      {Potion.HEALTH: 2, Potion.MANA: 2, Weapon.LONG_SWORD: 1})

    print('\nТест: перекладываем оружие')
    log, final = (
        begin.bind(show())
        .bind(equip(Weapon.LONG_SWORD))
        .bind(show())
        .bind(collect_log())
    ).run(start)
    print_log(log)

    print('\nТест: бой + пополняем здоровье')
    log, final = (
        begin.bind(show())
        .bind(drink_health())
        .bind(show())
        .bind(take_damage(40))
        .bind(show())
        .bind(drink_health())
        .bind(show())
        .bind(collect_log())
    ).run(start)
    print_log(log)

    print('\nТест: cмерть в бою')
    log, final = (
        begin.bind(show())
        .bind(take_damage(60))
        .bind(show())
        .bind(drink_health())
        .bind(show())
        .bind(equip(Weapon.LONG_SWORD))
        .bind(show())
        .bind(collect_log())
    ).run(start)
    print_log(log)
