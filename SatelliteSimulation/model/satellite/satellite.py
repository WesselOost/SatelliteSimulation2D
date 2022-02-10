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
import random
from abc import ABC
from SatelliteSimulation.model.basic_math.motion import CollisionDetecter, Trajectory

from SatelliteSimulation.model.disturbance.disturbance import Disturbance
from SatelliteSimulation.model.basic_math.math_basic import *
from SatelliteSimulation.model.basic_math.vector import *
from SatelliteSimulation.model.colllision.collision_avoidance import CollisionAvoidanceHandler
from SatelliteSimulation.model.satellite.satellite_velocity_handler import SatelliteVelocityHandler
from SatelliteSimulation.model.colllision.collision import Collision


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Satellite in general
# =========================================================================== #


class Satellite(ABC):
    """Abstract Satellite class should not be instantiated directly"""
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    satellite_id = 0


    def __init__(self, position: Vector, mass: float, size: int, observed_satellites: dict = {}):
        self.position: Vector = position
        Satellite.satellite_id += 1
        self.satellite_id = Satellite.satellite_id
        # TODO define max nav value with mass
        self.velocity: SatelliteVelocityHandler = SatelliteVelocityHandler(max_navigation_velocity_magnitude=4)
        self.__is_crashed: bool = False
        self.__observance_radius: int = 100
        self.__mass = mass
        self.__size = size
        self.__observed_satellites: dict = observed_satellites
        self.__possible_collisions: dict = {}
        self.__disturbances: list = []


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def mass(self) -> float:
        return self.__mass


    def size(self) -> int:
        return self.__size


    def surface(self) -> float:
        return (self.__size / 2) * math.pi


    def observed_satellites(self) -> dict:
        return self.__observed_satellites


    def possible_collisions(self) -> dict:
        return self.__possible_collisions


    def center(self) -> Vector:
        return Vector(self.position.x() + self.radius(), self.position.y() + self.radius())


    def radius(self) -> float:
        return self.__size / 2


    def observance_radius(self) -> float:
        return self.__observance_radius


    def is_crashed(self) -> bool:
        return self.__is_crashed


    def append_disturbance(self, disturbance: Disturbance):
        self.__disturbances.append(disturbance)


    def get_id(self) -> int:
        return self.satellite_id


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def __str__(self):
        return f'{self.__class__.__name__} id={self.satellite_id} center={self.center()}, velocity={self.velocity.value()}, radius={self.radius()}'


    def update_crashed_status(self):
        if not self.__is_crashed:
            self.__is_crashed = True
            self.velocity.navigation_velocity().clear()


    def update_observed_satellites(self, satellites: dict):
        self.__observed_satellites = satellites


    def move(self, delta_time: float):
        self.velocity.update_velocities(self.__disturbances)
        self.__disturbances = [disturbance for disturbance in self.__disturbances if disturbance.velocity().t() > 0]

        # TODO: use delta_time
        self.position.add_to_x(self.velocity.value().x())
        self.position.add_to_y(self.velocity.value().y())


    def navigate_to(self, direction_in_degrees: float):
        """
                  north 90
        west 180          east 0 (360)
                 south 270

        :param direction_in_degrees:
        :return:
        """
        angle_in_radians = np.math.radians(direction_in_degrees)
        max_nav_velocity = self.velocity.max_navigation_velocity()
        x = max_nav_velocity * np.math.cos(angle_in_radians)
        y = max_nav_velocity * np.math.sin(angle_in_radians)
        self.velocity.set_navigation_velocity(Vector(x, y))
        self.velocity.navigation_velocity().solve_equation_and_set_v1_v2(self.velocity.max_navigation_velocity(), 20)

    def navigate_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        # todo fix navigation duration
        self.velocity.navigation_velocity().solve_equation_and_set_v1_v2(self.velocity.max_navigation_velocity(), 20)
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



    def update_possible_collisions(self):
        possible_collisions: dict = dict()
        for observed_satellite in self.__observed_satellites:
            recored_positions: list = self.__observed_satellites[observed_satellite]
            record_amount = len(recored_positions)
            if record_amount >= 2:
                min_distance = self.radius() + observed_satellite.radius()
                observed_trajectory: Trajectory = Trajectory(recored_positions)
                satellite_trajectory: Trajectory = Trajectory(
                    [(0, 0)] * record_amount)
                if self.velocity.value().magnitude() != 0:
                    future_positions = [self.center()]
                    for i in range(record_amount-1):
                        new_position = add(future_positions[-1], self.velocity.dummy_update(i))
                        future_positions.append(new_position)
                    satellite_trajectory: Trajectory = Trajectory([p.get_as_tuple() for p in future_positions])
                collision = CollisionDetecter(min_distance, future_positions, satellite_trajectory)
                if collision:
                    possible_collisions[observed_satellite] = collision
        self.__possible_collisions = possible_collisions

    def avoid_possible_collisions(self):
        # Test collision avoidance
        first_key = list(self.__possible_collisions)[0]
        point_to_avoid: Vector = self.__possible_collisions[first_key].position()

        # self.__avoid_observed_satellite_direction_by_90_degrees()
        self.__avoid_collision_by_random_position()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


    def __avoid_collision_by_random_position(self):
        self.navigate_to(random.randint(0, 360))

        # todo create own class for avoiding methods

        pass


    def __avoid_observed_satellite_direction_by_90_degrees(self, observed_satellite_direction: Vector,
                                                           observed_satellite_center: Vector):
        handler = CollisionAvoidanceHandler(self.center(), observed_satellite_center, observed_satellite_direction)
        self.navigate_to(handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees())


    def __avoid_collision_by_increasing_distance_relative_to_all_observed_objects(self):
        pass


    def __avoid_collision_by_increasing_distance_relative_to_all_observed_objects_weighted(self):
        pass


    def __avoid_collision_by_inverting_direction(self):
        pass


    def get_type(self) -> int:
        """Override in child classes"""
        pass

# =========================================================================== #
#  SECTION: Satellite types A-D + SpaceJunk
# =========================================================================== #


class SatelliteA(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=100, size=size)


    def get_type(self) -> int:
        return 1


class SatelliteB(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=80, size=size)

    def get_type(self) -> int:
        return 2


class SatelliteC(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=120, size=size)

    def get_type(self) -> int:
        return 3

class SatelliteD(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=40, size=size)

    def get_type(self) -> int:
        return 4

class SpaceJunk(Satellite):
    def __init__(self, position: Vector, size: int):
        super().__init__(position, mass=10, size=size)
        self.update_crashed_status()

    def get_type(self) -> int:
        return 5


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


if __name__ == '__main__':
    pass
