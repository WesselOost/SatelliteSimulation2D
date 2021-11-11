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
import random

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
from SatelliteSimulation.model.math.vector import Vector
from SatelliteSimulation.model.math.velocity import Velocity


class Disturbance:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, reference_value: float = 0):
        # duration in frames
        self.__duration = random.randrange(60, 120, 1)

        # value vector in Pixel
        random_x = random.uniform(-1, 1) * random.randint(0, 5)
        random_y = random.uniform(-1, 1) * random.randint(0, 5)
        self.__velocity: Velocity = Velocity(random_x, random_y, acceleration=Vector(random_x, random_y).magnitude())

        self.__reference_value = reference_value

        self.__binary_direction = random.uniform(-1, 1)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def set_reference_value(self, ref: float):
        # TODO why is this reference value necessary?
        self.__reference_value = ref


    def velocity(self) -> Velocity:
        return self.__velocity


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def apply_malfunction(self, satellites, scale_factor: float):
        try:
            satellite = random.choice([satellite for satellite in satellites if not satellite.is_crashed()])

            if satellite.disturbance_duration() < self.__duration:
                satellite.set_disturbance_duration(self.__duration)

            satellite.velocity.disturbance_velocity().add_vector(Vector(self.__velocity.x() * scale_factor,
                                                                 self.__velocity.y() * scale_factor))
        except IndexError:
            # TODO everything is crashed, game over (maybe game over screen :p)
            pass


    def apply_gravitational_disturbance(self, satellites: list):
        for satellite in satellites:
            satellite.set_disturbance_duration(self.__duration)
            satellite.velocity.disturbance_velocity().set_y(self.__change_gravity(satellite.mass()))


    def apply_radiation_disturbance(self, satellites: list):
        for satellite in satellites:
            satellite.set_disturbance_duration(self.__duration)
            velocity_x: float = self.__velocity.x() * self.__add_radiation_pressure(satellite.surface())
            velocity_y: float = self.__velocity.y() * self.__add_radiation_pressure(satellite.surface())
            satellite.velocity.disturbance_velocity().set_xy(velocity_x, velocity_y)


    def apply_magnetic_disturbance(self, satellites):
        for satellite in satellites:
            satellite.set_disturbance_duration(self.__duration)
            velocity_x = self.__velocity.x() * self.__add_magnetic_disturbance(satellite.mass())
            velocity_y = self.__velocity.y() * self.__add_magnetic_disturbance(satellite.mass())
            satellite.velocity.disturbance_velocity().set_xy(velocity_x, velocity_y)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __change_gravity(self, mass: int) -> float:
        # LAW: F_G = G * (M*m)/r^2, M>m
        # with G, m = const and r~const (because shift is to little)
        # => F_G = const * M
        # heavier objects should be more influenced by the force
        # TODO check if r is making a big difference
        return (mass / self.__reference_value) * self.__binary_direction


    def __add_radiation_pressure(self, surface: int) -> float:
        # Radiation pressure from the sun
        if self.__velocity.x() != 0 and self.__velocity.y() != -1:
            return (self.__reference_value / surface) * 0.1
        x: float = random.uniform(-1, 1) * random.randint(0, 5)
        y: float = random.uniform(-1, 1) * random.randint(0, 5)
        self.__velocity.set_xy(x, y)
        return (surface / self.__reference_value) * 0.1


    def __add_magnetic_disturbance(self, mass: int) -> float:
        # assumption a satellite with more mass contains more metal
        # and more charge => is more attracted to the magnetic force
        # of the earth
        # TODO compare the gravity/magnetic disturbance which is
        return mass / self.__reference_value * 0.3
    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


if __name__ == '__main__':
    pass
