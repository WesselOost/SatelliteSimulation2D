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
from SatelliteSimulation.model.disturbance.disturbance import Disturbance
from SatelliteSimulation.model.math.math_basic import *
from SatelliteSimulation.model.math.vector import Vector

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Satellite in general
# =========================================================================== #
from SatelliteSimulation.model.satellite.satellite_velocity_handler import SatelliteVelocity


class Satellite:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, position: Vector, mass: float, size: int, observed_satellites: dict = {}):
        self.position: Vector = position
        # TODO define max nav value with mass
        self.velocity: SatelliteVelocity = SatelliteVelocity(max_navigation_velocity_magnitude=2)
        self.__is_crashed: bool = False
        self.__observance_radius: int = 30
        self.__disturbance_duration = 0
        self.__mass = mass
        self.__size = size
        self.__observed_satellites: dict = observed_satellites
        self.__previously_observed_satellites: dict = {}
        self.__disturbances: list = []


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def mass(self) -> float:
        return self.__mass


    def size(self) -> float:
        return self.__size


    def surface(self) -> float:
        return self.__size ** 2


    def observed_satellites(self) -> dict:
        return self.__observed_satellites


    def previously_observed_satellites(self) -> dict:
        return self.__previously_observed_satellites


    def center(self) -> Vector:
        return Vector(self.position.x() + self.radius(), self.position.y() + self.radius())


    def radius(self) -> float:
        return self.__size / 2


    def disturbance_duration(self) -> int:
        return self.__disturbance_duration


    def set_disturbance_duration(self, duration: float):
        self.__disturbance_duration = duration


    def observance_radius(self) -> float:
        return self.__observance_radius


    def is_crashed(self) -> bool:
        return self.__is_crashed


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def update_scale(self, scale_factor: float):
        self.__observance_radius *= scale_factor
        self.__size *= scale_factor
        self.position.set_vector(multiply(self.position, scalar=scale_factor))
        self.velocity.update_scale(scale_factor)

        if self.__disturbance_duration > 0:
            self.velocity.disturbance_velocity().set_vector(
                multiply(self.velocity.disturbance_velocity(), scalar=scale_factor))


    def update_crashed_status(self):
        if not self.__is_crashed:
            self.__is_crashed = True


    def update_observed_satellites(self, satellites: dict):
        self.__previously_observed_satellites = self.__observed_satellites
        self.__observed_satellites = satellites


    def clear_disturbance_duration(self):
        self.__disturbance_duration = 0


    def decrement_disturbance_duration(self):
        self.__disturbance_duration -= 1


    def move(self):
        for disturbance in self.__disturbances:
            pass
        # TODO add acceleration
        # self.velocity.update_velocities()
        self.position.add_to_x(self.velocity.value().x())
        self.position.add_to_y(self.velocity.value().y())


    def navigate_to(self, direction_in_degrees: int):
        angle_in_radians = np.math.radians(direction_in_degrees)
        max_nav_velocity = self.velocity.max_navigation_velocity()
        x = max_nav_velocity * np.math.cos(angle_in_radians)
        y = max_nav_velocity * np.math.sin(angle_in_radians)
        self.velocity.set_navigation_velocity(Vector(x, y))


    def navigate_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        self.velocity.navigation_velocity().set_acceleration(0.5)
        nav_x: float = self.velocity.navigation_velocity().x()
        nav_y: float = self.velocity.navigation_velocity().y()

        if pressed_left:
            self.velocity.set_navigation_velocity(Vector(-1, nav_y))
        if pressed_up:
            self.velocity.set_navigation_velocity(Vector(nav_x, -1))
        if pressed_right:
            self.velocity.set_navigation_velocity(Vector(1, nav_y))
        if pressed_down:
            self.velocity.set_navigation_velocity(Vector(nav_x, 1))


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
        for observed_satellite in self.__observed_satellites:
            if observed_satellite in previous_observed_satellites:
                previous_position: tuple = previous_observed_satellites[observed_satellite]
                current_position: tuple = self.observed_satellites()[observed_satellite]
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


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __get_satellite_trajectory(self) -> StraightLineEquation:
        # TODO shift center to outer edge
        point1: Vector = self.center()
        point2: tuple = (self.velocity.value().x() + point1.x(), self.velocity.value().y() + point1.y())
        return StraightLineEquation(point1.get_as_tuple(), point2)


    def __get_parallel_trajectory(self, shift: float) -> tuple:
        # TODO return StraightLineEquations that are parallel to the given
        # in a +/- shift
        return self.__get_satellite_trajectory(), self.__get_satellite_trajectory()


    def __avoid_collision_by_random_position(self):
        # todo create own class for avoiding methods
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
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=100, size=size)


class SatelliteB(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=80, size=size)


class SatelliteC(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=120, size=size)


class SatelliteD(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=40, size=size)


class SpaceJunk(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=10, size=size)
        self.update_crashed_status()


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


if __name__ == '__main__':
    pass
