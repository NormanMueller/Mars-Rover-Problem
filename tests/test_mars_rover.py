import pytest
from unittest.mock import Mock, patch, MagicMock, call
from unittest import TestCase
from mars_rover_problem import FactoryProcess, MarsRoboter, Direction, set_coordinate_system

@pytest.fixture
def coordinate_system ():
    coordinate_system_instance = set_coordinate_system(3,3)
    return coordinate_system_instance

def test_set_coordinate_system( ):
        #WHEN
        coordinate_system = set_coordinate_system(3,3)
        #THEN
        assert coordinate_system[-1] == (3,3)  # assert top right corner
        assert coordinate_system[0] == (0,0)   # assert bottom left corner
        assert len(coordinate_system) == 16    # assert length

#switch to unittest framework maybe more useful in this case, wanted to try both  -> not consistent 
class TestMarsRoboter(TestCase): 
    def setUp(self):
        self.mars_roboter = MarsRoboter([1, 1, Direction.N], coordinate_system)
    
    def test_move_to_north(self):
        #GIVEN
        self.mars_roboter.angle = 360
        #WHEN
        self.mars_roboter.move()
        #THEN
        assert self.mars_roboter.position == [1,2]

    def test_move_to_south(self):
        #GIVEN
        self.mars_roboter.angle = 180
        #WHEN
        self.mars_roboter.move()
        #THEN
        assert self.mars_roboter.position == [1,0]
    
    def test_move_to_east(self):
        #GIVEN
        self.mars_roboter.angle = 90
        #WHEN
        self.mars_roboter.move()
        #THEN
        assert self.mars_roboter.position == [2,1]
    
    def test_move_to_west(self):
        #GIVEN
        self.mars_roboter.angle = 270
        #WHEN
        self.mars_roboter.move()
        #THEN
        assert self.mars_roboter.position == [0,1]
    
    def test_turn_right(self):
        #GIVEN
        self.mars_roboter.angle = 360
        #WHEN
        self.mars_roboter.turn_right()
        #THEN
        assert self.mars_roboter.angle == 90
    
    def test_turn_left(self):
        #GIVEN
        self.mars_roboter.angle = 360
        #WHEN
        self.mars_roboter.turn_left()
        #THEN
        assert self.mars_roboter.angle == 270
