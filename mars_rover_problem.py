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


class CoordinateSystem:
    def __init__(self, x_coordinate: int, y_coordinate: int) -> None:
        self.x_coordinate: int = x_coordinate
        self.y_coordinate: int = y_coordinate
        self.coordinate_system: Tuple[int, int] = self.set_coordinate_system()

    def set_coordinate_system(self) -> None:
        coordinates = []
        for x in range(self.x_coordinate + 1):
            for y in range(self.y_coordinate + 1):
                coordinates.append((x, y))
        print(f"coordinate_system wurde erstellt: {coordinates[-1]}")

        return coordinates

### Dict to match direction and angle
direction_angle = {
        "Direction.N": [0, 360],
        "Direction.E": [90],
        "Direction.S": [180],
        "Direction.W": [270],
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
    def __init__(
        self, startpoint: List[any], coordinate_system: CoordinateSystem, 
        direction_angle:Dict[Direction, List],
        angle_direction:Dict[str,Direction]
    ) -> None:
        super(Roboter, self).__init__()
        self.position: List[int, int] = startpoint[:2]
        self.direction: Direction = startpoint[2]
        self.coordinate_system: CoordinateSystem = coordinate_system
        self.direction_angle =direction_angle
        self.angle_direction = angle_direction
    
    def get_current_angle(self) -> int:
        # match angle and direction
        angle = self.direction_angle.get(str(self.direction)) 
        return angle

    def turn_left(self) -> None:
        angle = self.get_current_angle()
        new_angle = max(angle) -90 # In case of North max entry 360 / add 90 degree
        self.direction = self.angle_direction.get(str(new_angle))

    def turn_right(self) -> None:
        angle = self.get_current_angle()
        new_angle = min(angle) +90 # In case of North min entry 0 / add -90 degree
        self.direction = self.angle_direction.get(str(new_angle))

    def move(self) -> None:
        """Move exactly 1 field in current direction"""
        if self.direction == Direction.N:
            self.position[1] = self.position[1] + 1
        elif self.direction == Direction.E:
            self.position[0] = self.position[0] + 1
        elif self.direction == Direction.S:
            self.position[1] = self.position[1] - 1
        elif self.direction == Direction.W:
            self.position[0] = self.position[0] - 1
        pass

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
    coordinate_system = CoordinateSystem(x_coordinate=5, y_coordinate=5)

    #### Roboter 1
    instruction_1 = "LMLMLMLMM"
    mars_roboter_instance_1 = MarsRoboter(
        startpoint=[1, 2, Direction.N], coordinate_system=coordinate_system,
        direction_angle =direction_angle,
        angle_direction = angle_direction
    )

    #### Roboter 2
    mars_roboter_instance_2 = MarsRoboter(
        startpoint=[3, 3, Direction.E], coordinate_system=coordinate_system,
        direction_angle=direction_angle,
        angle_direction=angle_direction
    )
    instruction_2 = "MMRMMRMRRM"

    ### Process
    process = FactoryProcess(
        mars_roboters=[mars_roboter_instance_1, mars_roboter_instance_2],
        instructions=[instruction_1, instruction_2],
    )
    process.handle()
