# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Disturbances that can occur in space
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import copy
import random
from SatelliteSimulation.model.basic_math.vector import Vector, multiply
from SatelliteSimulation.model.basic_math.velocity import Velocity


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class Disturbance:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self):
        # duration in frames
        self._duration: int = random.randrange(60, 120, 1)

        # value vector in Pixel
        self._velocity: Velocity = Velocity(0, 0)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def velocity(self) -> Velocity:
        return self._velocity


    def _set_velocity_trajectory(self, v_max: float):
        self._velocity.solve_equation_and_set_v1_v2(v_max=v_max, t_vertex=self._duration / 2)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def _random_value(self) -> float:
        return random.uniform(-1, 1) * random.randint(1, 5)


# ----------------------------------------------------------------------- #
#  SUBSECTION: Private Methods
# ----------------------------------------------------------------------- #

# =========================================================================== #
#  SECTION: Disturbance types
# =========================================================================== #


class Malfunction(Disturbance):
    def __init__(self):
        super().__init__()
        self.velocity().set_vector(Vector(x=self._random_value(), y=self._random_value()))
        self._set_velocity_trajectory(random.randint(1, 3))


class SolarRadiationDisturbance(Disturbance):
    def __init__(self, max_surface: float):
        super().__init__()
        self.__max_surface = max_surface
        self.__strength = random.randint(50, 100)

        velocity_x: float = self._random_value()
        velocity_y: float = self._random_value()
        self._velocity.set_xy(velocity_x, velocity_y)


    def update_trajectory(self, surface: float):
        # TODO use vector multiply
        # velocity_x: float = self._velocity.x() * self.__add_radiation_pressure(surface)
        # velocity_y: float = self._velocity.y() * self.__add_radiation_pressure(surface)
        # self._velocity.set_xy(velocity_x, velocity_y)
        self._set_velocity_trajectory(self.__radiation_pressure(surface))


    def __radiation_pressure(self, surface: float) -> float:
        return (surface / self.__max_surface) * self.__strength


class GravitationalDisturbance(Disturbance):
    def __init__(self, max_mass: float):
        super().__init__()
        self._max_mass = max_mass
        self._strength = random.randint(2, 4)
        self._velocity.set_y(self._random_value())


    def update_trajectory(self, mass: float):
        self._set_velocity_trajectory(self.__change_gravity(mass))


    def __change_gravity(self, mass: float) -> float:
        # LAW: F_G = G * (M*m)/r^2, M>m
        # with G, m = const and r~const (because shift is to little)
        # => F_G = const * M
        # heavier objects should be more influenced by the force
        # TODO check if r is making a big difference
        return (mass / self._max_mass) * self._strength


class MagneticDisturbance(GravitationalDisturbance):
    def __init__(self, max_mass: float):
        super().__init__(max_mass)
        self._velocity.set_x(self._random_value())


    def update_trajectory(self, mass: float):
        self._set_velocity_trajectory(self.__magnetic_disturbance(mass))


    def __magnetic_disturbance(self, mass: float) -> float:
        # assumption a satellite with more mass contains more metal
        # and more charge => is more attracted to the magnetic force
        # of the earth
        # TODO compare the gravity/magnetic disturbance which is
        return mass / self._max_mass * self._strength


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


if __name__ == '__main__':
    pass
