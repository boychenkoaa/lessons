"""Два стиля реакции на нехватку в одной цепочке."""

from robot import (
    SOAP,
    Move,
    RobotContext,
    RobotInfra,
    RobotState,
    SetState,
    Stop,
    switch2water_and_move,
)

"""
тестим логику обработки ошибок
если пены / воды меньше чем длина перемещения -- 2 варианта
сначала switch2water - включается вода и робот двигается
потом снова включаем пену
и пытаемся поехать, но next уже просто лямбда с остановом если пены было мало
последний Mоve не выполнится
"""

ast = Move(
    20,  # пены 15 < 20 - переключится на воду
    next=lambda ctx: switch2water_and_move(  # проедет на воде в точку (20, 0)
        ctx,
        nxt=lambda ctx: SetState(
            SOAP,
            next=lambda ctx: Move(
                20,  # пены по прежнему 15 < 20
                next=lambda ctx: (
                    Stop()  # тут завершится выполнение
                    if ctx.infra.response != "OK"
                    else Move(100, next=lambda ctx: Stop())  # не выполнится
                ),
            ),
        ),
        distance=20,
    ),
)

ctx = RobotContext(
    state=RobotState(x=0.0, y=0.0, angle=0, state=SOAP, water_qty=50, soap_qty=15),
    infra=RobotInfra(log=(), response=None),
)

print("start:", ctx)
final = ast.interpret(ctx)
print("final:", final)
