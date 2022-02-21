# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-11-16 13:16:31
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Collision object consisting out of the point and the time of collision
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from SatelliteSimulation.model.basic_math.vector import *


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class FutureCollisionData:
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, point_of_crash: tuple, moment_of_crash: float, trajectory):
        self.__x = point_of_crash[0]
        self.__y = point_of_crash[1]
        self.__observed_trajectory = trajectory
        self.__moment_of_crash = moment_of_crash


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def position(self) -> Vector:
        return Vector(self.__x, self.__y)


    def time(self) -> float:
        return self.__moment_of_crash

    @property
    def trajectory(self):
        return self.__observed_trajectory


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def __str__(self) -> str:
        return f"Collision ({self.__x}, {self.__y}) in {self.__moment_of_crash}frames"
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


if __name__ == '__main__':
    pass
