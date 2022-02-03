# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Class description
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from SatelliteSimulation.model.arrow import Arrow
from SatelliteSimulation.model.basic_math.vector import *
from SatelliteSimulation.model.basic_math.velocity import Velocity

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #



# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class SatelliteVelocityHandler:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, max_navigation_velocity_magnitude: float):
        self.__navigation_velocity: Velocity = Velocity(0, 0)
        self.__max_navigation_velocity_magnitude: float = max_navigation_velocity_magnitude
        self.__disturbance_velocity: Velocity = Velocity(0, 0)
        self.__collision_velocity: Velocity = Velocity(0, 0)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def navigation_velocity(self) -> Velocity:
        return self.__navigation_velocity


    def max_navigation_velocity(self) -> float:
        return self.__max_navigation_velocity_magnitude


    def set_navigation_velocity(self, velocity: Vector):
        if velocity.magnitude() <= self.__max_navigation_velocity_magnitude:
            self.__navigation_velocity.set_vector(velocity)


    def disturbance_velocity(self) -> Velocity:
        return self.__disturbance_velocity


    def collision_velocity(self) -> Velocity:
        return self.__collision_velocity


    def value(self) -> Vector:
        return add(self.__navigation_velocity, add(self.__disturbance_velocity, self.__collision_velocity))


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def update_velocities(self, disturbances: list):
        self.__disturbance_velocity.clear()
        for disturbance in disturbances:
            disturbance.velocity().update()
            self.__disturbance_velocity.add_vector(disturbance.velocity())
        # if self.__disturbance_velocity.magnitude() > 0:
        #     logging.debug(f'disturbance magnitude {self.disturbance_velocity().magnitude()}')

        self.__navigation_velocity.update()
        self.__collision_velocity.update()


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
