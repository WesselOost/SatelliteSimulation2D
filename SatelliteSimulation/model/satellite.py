#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-27 12:54:01
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
a bunch of possible satellites and their abilities
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #

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
from SatelliteSimulation.model.mathBasics import StraightLineEquation, LinearSystemOfEquations


class Satellite:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: int, y: int, weight: int, size: int, observedSatellites: dict = {}):
        self.is_crashed: bool = False  # is the
        self.observance_radius: int = 75
        self.danger_zone_shift: int = 20
        self.x = x
        self.y = y
        self.disturbance_duration = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_navigation_velocity: float = 75 / weight
        self.weight = weight
        self.surface = size * size
        self.size = size
        self.danger_zone_radius = self.size // 2 + self.danger_zone_shift
        self.observed_satellites: dict = observedSatellites


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def get_center(self) -> tuple:
        return self.x + self.size / 2, self.y + self.size / 2


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def check_satellite_status(self):
        if not self.is_crashed:
            for satellite in self.observed_satellites:
                outer_border = self.size / 2 + satellite.size / 2
                if calculate_distance(self.get_center(), satellite.get_center()) <= outer_border:
                    self.is_crashed = True


    def collision_possible(self, point1: tuple, point2: tuple, size: float) -> bool:
        satellite_trajectory = self.__get_satellite_trajectory()
        other_satellite_trajectories = [StraightLineEquation(point1, point2)]
        other_satellite_trajectories.extend(self.__get_parallel_trajectory(size))
        lgs = LinearSystemOfEquations()
        for trajectory in other_satellite_trajectories:
            intersection = lgs.get_intersection(satellite_trajectory, trajectory)


    def detect_possible_collisions(self, previous_observed_satellites) -> dict:
        possible_collisions: dict = dict()
        lgs = LinearSystemOfEquations()
        satellite_trajectory = self.__get_satellite_trajectory()
        for observed_satellite in self.observed_satellites:
            if observed_satellite in previous_observed_satellites:
                previous_position: tuple = previous_observed_satellites[observed_satellite]
                current_position: tuple = self.observed_satellites[observed_satellite]
                observed_trajectories = [StraightLineEquation(previous_position, current_position)]
                observed_trajectories.extend(self.__get_parallel_trajectory(observed_satellite.size))
                # TODO 4 straightLineEquations
                for observed_trajectory in observed_trajectories:
                    intersection = lgs.get_intersection(observed_trajectory, satellite_trajectory)
                    # TODO check collinear vectors
                    if intersection != (float('inf'), float('inf')):
                        observed_t = observed_trajectory.calculate_t(intersection)
        return possible_collisions


    def avoid_possible_collisions(self, possible_collisions: dict):
        pass
        # first_collision = next(iter(possible_collisions))


    def navigateTo(self, direction_in_degrees: int):
        angle_in_radians = np.math.radians(direction_in_degrees)

        self.x += (self.max_navigation_velocity * np.math.cos(angle_in_radians))
        self.y += (self.max_navigation_velocity * np.math.sin(angle_in_radians))


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __get_satellite_trajectory(self) -> StraightLineEquation:
        # TODO shift center to outer edge
        point1 = self.get_center()
        point2 = self.velocity_x + point1[0], self.velocity_y + point1[1]
        return StraightLineEquation(point1, point2)


    def __get_parallel_trajectory(self, shift: float) -> tuple:
        # TODO return StraightLineEquations that are parallel to the given
        # in a +/- shift
        return self.__get_satellite_trajectory(), self.__get_satellite_trajectory()


    def __avoid_collision_by_random_position(self):
        pass


    def __avoid_collision_by_90_degrees_angle(self):
        pass


    def __avoid_collision_by_increasing_distance_relative_to_all_observed_objects(self):
        pass


    def __avoid_collision_by_increasing_distance_relative_to_all_observed_objects_weighted(self):
        pass


    def __avoid_collision_by_inverting_direction(self):
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
        self.is_crashed = True


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


def calculate_distance(coord_A: tuple, coords_B: tuple) -> float:
    return np.math.sqrt((coords_B[0] - coord_A[0]) ** 2 + (coords_B[1] - coord_A[1]) ** 2)


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


if __name__ == '__main__':
    pass
