from robot import (
    SOAP,
    WATER,
    RobotState,
    StateMonad,
    inc_water,
    move,
    reset,
    set_state,
    start,
    stop,
    turn,
)

# программа для робота с восстановлением из ошибочного состояния
# reset сбрасывает ошибку, вызванную включением воды при пустом контейнере
s = StateMonad(RobotState(0.0, 0.0, 0, WATER, water_qty=100, soap_qty=0))
result = (
    s.bind(set_state(WATER))
    .bind(inc_water(-100))
    .bind(set_state(WATER))
    .or_else(reset())
    .bind(inc_water(50))
    .bind(set_state(WATER))
)

print(f"State: {result.state}")
print(f"Infra: {result.infra}")
