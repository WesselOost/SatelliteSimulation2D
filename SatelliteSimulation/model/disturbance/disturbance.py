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
        self._duration = random.randrange(60, 120, 1)

        # value vector in Pixel
        self._velocity: Velocity = Velocity(0, 0)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def velocity(self) -> Velocity:
        return self._velocity


    def set_velocity_trajectory(self, v_max:float):
        self._velocity.solve_equation_and_set_v1_v2(v_max=v_max, t_vertex=self._duration / 2)


    def _random_value(self)-> float:
        return random.uniform(-1, 1) * random.randint(0, 5)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

# ----------------------------------------------------------------------- #
#  SUBSECTION: Private Methods
# ----------------------------------------------------------------------- #

# =========================================================================== #
#  SECTION: Disturbance types
# =========================================================================== #


class Malfunction(Disturbance):
    def __init__(self, scale_factor: float):
        super().__init__()
        self.velocity().set_vector(multiply(Vector(x=self._random_value(), y=self._random_value()), scale_factor))
        self.set_velocity_trajectory(random.randint(1, 3) * scale_factor)


class SolarRadiationDisturbance(Disturbance):
    def __init__(self, max_surface: float, scale_factor: float):
        super().__init__()
        self.__max_surface = max_surface
        self.__scale_factor = scale_factor
        self.__radiation_strength = random.randint(50, 100)

        velocity_x: float = self._random_value() * scale_factor
        velocity_y: float = self._random_value() * scale_factor
        self._velocity.set_xy(velocity_x, velocity_y)


    def update_surface(self, surface: float):
        #TODO use vector multiply
        # velocity_x: float = self._velocity.x() * self.__add_radiation_pressure(surface)
        # velocity_y: float = self._velocity.y() * self.__add_radiation_pressure(surface)
        # self._velocity.set_xy(velocity_x, velocity_y)
        self.set_velocity_trajectory(self.__add_radiation_pressure(surface) * self.__scale_factor)


    def __add_radiation_pressure(self, surface: float) -> float:
        return (surface / self.__max_surface) * self.__radiation_strength


    # # #TODO fix copy disturbance.
    # def __deepcopy__(self, memodict={}):
    #
    #
    # def __copy__(self):
    #     disturbance = type(self)(self.__max_surface, self.__scale_factor)
    #     disturbance.__dict__.update(self.__dict__)
    #     return disturbance


class GravitationalDisturbance(Disturbance):
    def __init__(self, max_mass: float, mass: float, scale_factor: float):
        super().__init__()
        self.__max_mass = max_mass
        self.__binary_direction = random.uniform(-1, 1)
        self._velocity.set_y(self.__change_gravity(mass) * scale_factor)


    def __change_gravity(self, mass: float) -> float:
        # LAW: F_G = G * (M*m)/r^2, M>m
        # with G, m = const and r~const (because shift is to little)
        # => F_G = const * M
        # heavier objects should be more influenced by the force
        # TODO check if r is making a big difference
        return (mass / self.__max_mass) * self.__binary_direction


class MagneticDisturbance(Disturbance):
    def __init__(self, max_mass: float, mass: float, scale_factor: float):
        super().__init__()
        self.__max_mass = max_mass
        velocity_x = self._velocity.x() * self.__add_magnetic_disturbance(mass) * scale_factor
        velocity_y = self._velocity.y() * self.__add_magnetic_disturbance(mass) * scale_factor
        self._velocity.set_xy(velocity_x, velocity_y)


    def __add_magnetic_disturbance(self, mass: float) -> float:
        # assumption a satellite with more mass contains more metal
        # and more charge => is more attracted to the magnetic force
        # of the earth
        # TODO compare the gravity/magnetic disturbance which is
        return mass / self.__max_mass * 0.3


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


if __name__ == '__main__':
    pass
