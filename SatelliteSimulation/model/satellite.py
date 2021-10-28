#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-27 12:54:01
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
a bunch of possbible satellites and their abilities
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #

from SatelliteSimulation.model.model import *
from mathBasics import *
import numpy as np 


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Satellite in general
# =========================================================================== #


class Satellite:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: int, y: int, weight: int, size: int, visibleSatellites: list = []):
        self.isCrashed: bool = False  # is the
        self.observanceRadius: int = 75
        self.dangerZoneShift: int = 20
        self.x = x
        self.y = y
        self.disturbance_duration = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.weight = weight
        self.surface = size * size
        self.size = size
        self.dangerZoneRadius = self.size // 2 + self.dangerZoneShift
        self.visible_satellites: list = visibleSatellites

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def get_center(self) -> tuple:
        return self.x+self.size/2, self.y+self.size/2

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def moveTo(self, new_x: int, new_y: int):
        pass

    def check_satellite_status(self):
        if not self.isCrashed:
            for satellite in self.visible_satellites:
                outer_boarder = self.size/2 + satellite.size/2
                if calculate_distance(self.get_center(), satellite.get_center()) <= outer_boarder:
                    self.isCrashed = True

    def collision_possible(self, point1:tuple, point2:tuple, size:float)->bool:
        satellite_trajectory = self.__get_satellite_trajectory()
        other_satellite_trajectories = [StraightLineEquation(point1, point2)]
        other_satellite_trajectories.extend(self.__get_parallel_trajectory(size))
        lgs = LinearSystemOfEquations()
        for trajectory in other_satellite_trajectories:
            intersection = lgs.get_intersection(satellite_trajectory, trajectory)
        
    
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __get_satellite_trajectory(self)->StraightLineEquation:
        point1 = self.get_center()
        point2 = self.velocity_x+point1[0], self.velocity_y+point1[1]
        return StraightLineEquation(point1, point2)

    def __get_parallel_trajectory(self, shift: float) ->tuple:
        #TODO return StraightLineEquations that are parallel to the given 
        # in a +/- shift
        pass
        
# =========================================================================== #
#  SECTION: Satellite types A-D
# =========================================================================== #


class SatelliteA(Satellite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, weight=100, size=size)


class SatelliteB(Satellite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, weight=80, size=size)


class SatelliteC(Satellite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, weight=120, size=size)


class SatelliteD(Satellite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, weight=40, size=size)
        

class SpaceJunk(Satellite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x, y, weight=10, size=size)
        self.isCrashed = True



# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


def calculate_distance(coord_A: tuple, coords_B: tuple) -> float:
    return math.sqrt((coords_B[0] - coord_A[0]) ** 2 + (coords_B[1] - coord_A[1]) ** 2)

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


if __name__ == '__main__':
    pass
