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


### Dict to match direction and angle
direction_angle = {
    "Direction.N": 360,
    "Direction.E": 90,
    "Direction.S": 180,
    "Direction.W": 270,
}

### Dict to match angle and movement
# move to north means y +=1 and x +=0 -> [0.1]
angle_move = {
    "360": [0, 1],
    "0": [0, 1],
    "90": [1, 0],
    "180": [0, -1],
    "270": [-1, 0],
}


class MarsRoboter(Roboter):
    def __init__(self, startpoint: List[any], coordinate_system: List[Tuple]) -> None:
        super(Roboter, self).__init__()
        self.position = startpoint[:2]
        self.direction = startpoint[2]
        self.angle = self.get_angle()
        self.coordinate_system = coordinate_system

    def get_angle(self) -> List[int]:
        # match direction and angle
        angle = direction_angle.get(str(self.direction))
        return angle

    def turn_left(self) -> None:
        new_angle = self.angle - 90  # In case of North max entry 360 / minus 90 degre
        self.angle = 360 - 90 if new_angle < 0 else new_angle

    def turn_right(self) -> None:
        new_angle = self.angle + 90  # In case of North min entry 0 / add90 degree
        self.angle = 0 + 90 if new_angle > 360 else new_angle

    def move(self) -> None:
        """Move exactly 1 field in current direction"""
        move = angle_move.get(str(self.angle))
        self.position[0] += move[0]
        self.position[1] += move[1]

    def get_position(self):
        self.angle = (360 if self.angle == 0 else self.angle )  # 360  degree and 0 result in north
        # map angle back to  direction
        self.direction = [k for k, v in direction_angle.items() if v == self.angle]
        print(f"Position: {self.position}, Direction: {self.direction[0]}, angle: {self.angle}")


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
