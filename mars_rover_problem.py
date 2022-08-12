from enum import Enum, auto
from typing import Dict, Set, List, Tuple
from abc import ABC, abstractclassmethod


class Direction(Enum):
    S = "SOUTH"
    N = "NORTH"
    W = "WEST"
    E = "EAST"


# interface  make it easy to implement another Roboter Type
class Roboter(ABC):
    @abstractclassmethod
    def turn_left(self):
        """turn left has to be defined"""
        pass

    @abstractclassmethod
    def turn_right(self):
        """turn right has to be defined"""
        pass

    @abstractclassmethod
    def move(self):
        """move has to be defined"""
        pass


def set_coordinate_system(x_coordinate, y_coordinate) -> List[Tuple[int, int]]:
    coordinates = []
    for x in range(x_coordinate + 1):
        for y in range(y_coordinate + 1):
            coordinates.append((x, y))
    return coordinates


### Dict to match direction and (angle, move)
# move to north means y +=1 and x +=0 -> [0.1]
direction_angle_movement = {
    "Direction.N": {"angle": [0, 360], "move": [0, 1]},
    "Direction.E": {"angle": [90], "move": [1, 0]},
    "Direction.S": {"angle": [180], "move": [0, -1]},
    "Direction.W": {"angle": [270], "move": [-1, 0]},
}

### Dict to match angle and direction
angle_direction = {
    "0": Direction.N,
    "360": Direction.N,
    "90": Direction.E,
    "180": Direction.S,
    "270": Direction.W,
}


class MarsRoboter(Roboter):
    def __init__(self, startpoint: List[any], coordinate_system: List[Tuple]) -> None:
        super(Roboter, self).__init__()
        self.position = startpoint[:2]
        self.direction = startpoint[2]
        self.coordinate_system = coordinate_system

    def get_current_angle(self) -> List[int]:
        # match direction and angle
        angle = direction_angle_movement.get(str(self.direction)).get("angle")
        return angle

    def turn_left(self) -> None:
        angle = self.get_current_angle()
        new_angle = max(angle) - 90  # In case of North max entry 360 / minus 90 degree
        self.direction = angle_direction.get(str(new_angle))

    def turn_right(self) -> None:
        angle = self.get_current_angle()
        new_angle = min(angle) + 90  # In case of North min entry 0 / add90 degree
        self.direction = angle_direction.get(str(new_angle))

    def move(self) -> None:
        """Move exactly 1 field in current direction"""
        move = direction_angle_movement.get(str(self.direction)).get("move")
        self.position[0] += move[0]
        self.position[1] += move[1]

    def get_position(self):
        print(f"Position: {self.position}, Direction: {self.direction}")


class FactoryProcess:
    """Process instructions for your mars mission"""
    def __init__(self, mars_roboters: List[MarsRoboter], instructions: List[str]):
        self.mars_roboters = mars_roboters
        self.instructions = instructions
        self.processed_mars_roboter: List[MarsRoboter] = None

    @staticmethod
    def execute_instructions(mars_roboter: MarsRoboter, instructions) -> MarsRoboter:
        for command in instructions:
            if command == "M":
                mars_roboter.move()
            elif command == "L":
                mars_roboter.turn_left()
            elif command == "R":
                mars_roboter.turn_right()
        return mars_roboter

    def handle(self) -> None:
        # excecute instruction for every mars roboter
        processed_roboter = []
        for mars_roboter, instruction in zip(self.mars_roboters, self.instructions):
            processed_roboter.append(
                self.execute_instructions(mars_roboter, instruction)
            )
        self.processed_mars_roboter = processed_roboter

        # return final position for every mars roboter
        for mars_roboter in self.processed_mars_roboter:
            mars_roboter.get_position()


if __name__ == "__main__":
    ### Coordinate System
    coordinate_system = set_coordinate_system(x_coordinate=5, y_coordinate=5)

    #### Roboter 1
    instruction_1 = "LMLMLMLMM"
    mars_roboter_instance_1 = MarsRoboter(
        startpoint=[1, 2, Direction.N], coordinate_system=coordinate_system
    )

    #### Roboter 2
    mars_roboter_instance_2 = MarsRoboter(
        startpoint=[3, 3, Direction.E], coordinate_system=coordinate_system
    )
    instruction_2 = "MMRMMRMRRM"

    ### Process
    process = FactoryProcess(
        mars_roboters=[mars_roboter_instance_1, mars_roboter_instance_2],
        instructions=[instruction_1, instruction_2],
    )
    process.handle()
