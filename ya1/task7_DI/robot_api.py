from interpret import Interpreter
from base import RobotPose
from programs import Rect, program_clean_rect
from robot import Robot, Cleaner, RobotTool
from robot_cmd import BASE_ROBOT_COMMANDS


class RobotClient:
    def __init__(
        self,
        interpreter: Interpreter,
    ):
        self._interpreter = interpreter
        self._connected = True

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def get_pos(self) -> tuple[float, float]:
        return self.robot.pos

    def get_orientation(self) -> float:
        return self.robot.orientation

    def get_tool(self) -> RobotTool:
        return self.robot.tool

    def run_program(self, program: list[str]):
        if not self._connected:
            print("Клиент не подключен")
            return
        self._interpreter.run(program)

    def clean_rect(self, rect: Rect, inset: float):
        pose = self._robot_pose
        program = program_clean_rect(pose, rect, inset)
        self.run_program(program)

    @property
    def robot(self) -> Robot:
        return self._interpreter.robot

    @property
    def _robot_pose(self) -> RobotPose:
        return self.robot.pose
        
# тут можно было добавить и фабрику, но для демонстрации DI хватит и одной фукнции-билдера...

def build_cleaner_client() -> RobotClient:
    cleaner = Cleaner()
    interpreter = Interpreter(cleaner, BASE_ROBOT_COMMANDS)
    return RobotClient(interpreter)
