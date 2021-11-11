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


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
from SatelliteSimulation.model.math.vector import Vector, add, multiply
from SatelliteSimulation.model.math.velocity import Velocity


class SatelliteVelocity:

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
    def update_velocities(self):
        disturbance_magnitude = self.__disturbance_velocity.magnitude()
        disturbance_acceleration = self.__disturbance_velocity.acceleration()
        if disturbance_magnitude != 0 or disturbance_acceleration > 0:
            self.__disturbance_velocity.set_vector(
                multiply(self.__disturbance_velocity,
                         disturbance_acceleration))

        navigation_magnitude = self.__navigation_velocity.magnitude()
        navigation_acceleration = self.__navigation_velocity.acceleration()
        if navigation_magnitude != 0 or navigation_acceleration > 0:
            self.set_navigation_velocity(
                multiply(self.__navigation_velocity,
                         navigation_acceleration))

        collision_velocity = self.__collision_velocity.magnitude()
        collision_acceleration = self.__collision_velocity.acceleration()
        if collision_velocity != 0 or collision_acceleration > 0:
            self.__collision_velocity.set_vector(
                multiply(self.__collision_velocity,
                         collision_acceleration))


    def update_scale(self, scale_factor):
        self.__max_navigation_velocity_magnitude *= scale_factor
        self.__collision_velocity.update_scale(scale_factor)
        self.__navigation_velocity.update_scale(scale_factor)
        self.__disturbance_velocity.update_scale(scale_factor)


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
