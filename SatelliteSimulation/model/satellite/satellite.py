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
from SatelliteSimulation.model.basic_math.motion import CollisionDetecter, Trajectory

from SatelliteSimulation.model.disturbance.disturbance import Disturbance
from SatelliteSimulation.model.basic_math.math_basic import *
from SatelliteSimulation.model.basic_math.vector import *
from SatelliteSimulation.model.satellite.satellite_velocity_handler import SatelliteVelocityHandler
from SatelliteSimulation.model.collision import Collision


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Satellite in general
# =========================================================================== #


class Satellite:

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


    def size(self) -> float:
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



    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def __str__(self):
        return f'{self.__class__.__name__} id={self.satellite_id} center={self.center()}, velocity={self.velocity.value()}, radius={self.radius()}'


    def update_scale(self, scale_factor: float):
        self.__observance_radius *= scale_factor
        self.__size *= scale_factor
        self.position.set_vector(multiply(self.position, scalar=scale_factor))
        self.velocity.update_scale(scale_factor)
        self.update_arrow()
        for disturbance in self.__disturbances:
            disturbance.velocity().set_vector(multiply(disturbance.velocity(), scalar=scale_factor))


    def update_crashed_status(self):
        if not self.__is_crashed:
            self.__is_crashed = True



    def update_observed_satellites(self, satellites: dict):
        self.__observed_satellites = satellites


    def move(self, delta_time:float):
        self.velocity.update_velocities(self.__disturbances)
        self.__disturbances = [disturbance for disturbance in self.__disturbances if disturbance.velocity().t() > 0]
        self.update_arrow()
        self.position.add_to_x(self.velocity.value().x() * delta_time)
        self.position.add_to_y(self.velocity.value().y() * delta_time)


    def update_arrow(self):
        velocity = self.velocity.value()
        if velocity.magnitude() != 0:
            unit_normal_direction_vector: Vector = self.velocity.value().unit_normal()

            start_vector: Vector = Vector(self.center().x() + self.radius() * unit_normal_direction_vector.x(),
                self.center().y() + self.radius() * unit_normal_direction_vector.y())

            self.velocity.update_velocity_arrow(start_vector)


    def navigate_to(self, direction_in_degrees: int):
        angle_in_radians = np.math.radians(direction_in_degrees)
        max_nav_velocity = self.velocity.max_navigation_velocity()
        x = max_nav_velocity * np.math.cos(angle_in_radians)
        y = max_nav_velocity * np.math.sin(angle_in_radians)
        self.velocity.set_navigation_velocity(Vector(x, y))
        self.velocity.navigation_velocity().solve_equation_and_set_v1_v2(self.velocity.max_navigation_velocity(), 20)

    def navigate_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        #todo fix navigation duration
        self.velocity.navigation_velocity().solve_equation_and_set_v1_v2(self.velocity.max_navigation_velocity(), 20)
        nav_x: float = self.velocity.navigation_velocity().x()
        nav_y: float = self.velocity.navigation_velocity().y()

        # TODO scale navigation
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

    def avoid_possible_collisions(self):
        # Test collision avoidance
        first_key = list(self.__possible_collisions)[0]
        point_to_avoid: Vector = self.__possible_collisions[first_key].position()
        # self.__avoid_collision_by_90_degrees_angle(point_to_avoid)
        # self.__avoid_collision_by_random_position()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


    def __avoid_collision_by_random_position(self):
        self.navigate_to(random.randint(0,360))

        # todo create own class for avoiding methods

        pass


    def __avoid_collision_by_90_degrees_angle(self, point_to_avoid: Vector):
        pass


    def __avoid_collision_by_increasing_distance_relative_to_all_observed_objects(self):
        pass


    def __avoid_collision_by_increasing_distance_relative_to_all_observed_objects_weighted(self):
        pass


    def __avoid_collision_by_inverting_direction(self):
        pass


# =========================================================================== #
#  SECTION: Satellite types A-D + SpaceJunk
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
