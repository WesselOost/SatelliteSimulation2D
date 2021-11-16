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
from SatelliteSimulation.model.math.vector import Vector
from SatelliteSimulation.model.math.velocity import Velocity
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
        random_x = random.uniform(-1, 1) * random.randint(0, 5)
        random_y = random.uniform(-1, 1) * random.randint(0, 5)
        self._velocity: Velocity = Velocity(random_x, random_y, acceleration=Vector(random_x, random_y).magnitude())


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def velocity(self) -> Velocity:
        return self._velocity

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
    def __init__(self):
        super().__init__()


    def apply_malfunction(self, satellites, scale_factor: float):
        try:
            satellite = random.choice([satellite for satellite in satellites if not satellite.is_crashed()])

            if satellite.disturbance_duration() < self._duration:
                satellite.set_disturbance_duration(self._duration)

            satellite.velocity.disturbance_velocity().add_vector(Vector(self._velocity.x() * scale_factor,
                                                                        self._velocity.y() * scale_factor))
        except IndexError:
            # TODO everything is crashed, game over (maybe game over screen :p)
            pass


class SolarRadiationDisturbance(Disturbance):
    def __init__(self, max_surface: float):
        super().__init__()
        self.__max_surface = max_surface


    def apply_disturbance(self, satellites: list):
        for satellite in satellites:
            satellite.set_disturbance_duration(self._duration)
            velocity_x: float = self._velocity.x() * self.__add_radiation_pressure(satellite.surface())
            velocity_y: float = self._velocity.y() * self.__add_radiation_pressure(satellite.surface())
            satellite.velocity.disturbance_velocity().set_xy(velocity_x, velocity_y)


    def __add_radiation_pressure(self, surface: int) -> float:
        # Radiation pressure from the sun
        if self._velocity.x() != 0 and self._velocity.y() != -1:
            return (self.__max_surface / surface) * 0.1
        x: float = random.uniform(-1, 1) * random.randint(0, 5)
        y: float = random.uniform(-1, 1) * random.randint(0, 5)
        self._velocity.set_xy(x, y)
        return (surface / self.__max_surface) * 0.1


class GravitationalDisturbance(Disturbance):
    def __init__(self, max_mass: float):
        super().__init__()
        self.__max_mass = max_mass
        self.__binary_direction = random.uniform(-1, 1)


    def apply_disturbance(self, satellites: list):
        for satellite in satellites:
            satellite.set_disturbance_duration(self._duration)
            satellite.velocity.disturbance_velocity().set_y(self.__change_gravity(satellite.mass()))


    def __change_gravity(self, mass: int) -> float:
        # LAW: F_G = G * (M*m)/r^2, M>m
        # with G, m = const and r~const (because shift is to little)
        # => F_G = const * M
        # heavier objects should be more influenced by the force
        # TODO check if r is making a big difference
        return (mass / self.__max_mass) * self.__binary_direction


class MagneticDisturbance(Disturbance):
    def __init__(self, max_mass: float):
        super().__init__()
        self.__max_mass = max_mass


    def apply_disturbance(self, satellites):
        for satellite in satellites:
            satellite.set_disturbance_duration(self._duration)
            velocity_x = self._velocity.x() * self.__add_magnetic_disturbance(satellite.mass())
            velocity_y = self._velocity.y() * self.__add_magnetic_disturbance(satellite.mass())
            satellite.velocity.disturbance_velocity().set_xy(velocity_x, velocity_y)


    def __add_magnetic_disturbance(self, mass: int) -> float:
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
