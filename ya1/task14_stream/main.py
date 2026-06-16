from application import Application
from base import CleaningMode, RobotState
from commands import MoveCommand, ResetCommand, SetStateCommand, TurnCommand


def main() -> None:
    app = Application(
        {
            "R1": RobotState(x=0.0, y=0.0, angle=0.0, state=CleaningMode.WATER.value),
            "R2": RobotState(x=10.0, y=0.0, angle=0.0, state=CleaningMode.WATER.value),
        }
    )

    # отправляем в перемешанном порядек
    # но при выполнении все равно в историю запишутся по роботам
    app.handle_command("R1", MoveCommand(10.0))
    app.handle_command("R2", TurnCommand(90.0))
    app.handle_command("R1", TurnCommand(90.0))
    app.handle_command("R2", MoveCommand(7.0))
    app.handle_command("R1", MoveCommand(5.0))
    app.handle_command("R2", SetStateCommand(CleaningMode.BRUSH))
    app.handle_command("R1", SetStateCommand(CleaningMode.SOAP))
    app.handle_command("R2", MoveCommand(3.0))

    # угол больше 360 - доменная ошибка
    app.handle_command("R2", TurnCommand(400.0))

    # попытка запустить корректную команду,
    # должен быть отказ (REJECTED)
    app.handle_command("R2", TurnCommand(180.0))

    # сброс после ошибки + валидная команда
    app.handle_command("R2", ResetCommand())
    app.handle_command("R2", TurnCommand(180.0))

    # завершаем
    app.shutdown()

    print("\n--- Общий лог всех событий ---\nR1")
    for event in app.event_log.get_events("R1"):
        print(f"  R1: {event.get_event_type()}")
    for event in app.event_log.get_events("R2"):
        print(f"  R2: {event.get_event_type()}")
    print("\nR2")
    print(f"R1: {app.get_state('R1')}")
    print(f"R2: {app.get_state('R2')}")

    print("\n --- Проверка undo / redo ---\nR1")
    print(f"  состояние после события [1]: {app.get_state_after('R1', 1)}")
    print(f"  undo до события [0] (исходное): {app.undo('R1', 0)}")

    print("\nR2")
    print(f"  состояние после события [2]: {app.get_state_after('R2', 2)}")
    print(f"  undo до события [2] (после [1]): {app.undo('R2', 2)}")


if __name__ == "__main__":
    main()
