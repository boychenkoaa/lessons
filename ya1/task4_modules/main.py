from interpret import Interpreter
from robot import Robot

if __name__ == "__main__":
    # тестовый прогон из упражнения
    program = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]
    robot = Robot()
    interpreter = Interpreter(robot)
    interpreter.run(program)
        
    # неправильный синтаксис
    program = [
        "move 100",
        "turn -90",
        "set MAGIC SWORD", # ошибка
        "start",
        "move 50",
        "stop",
    ]
    robot2 = Robot()
    interpreter = Interpreter(robot2)
    interpreter.run(program)
