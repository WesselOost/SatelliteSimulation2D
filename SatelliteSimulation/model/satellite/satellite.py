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
    def __init__(self, position: Vector, mass: float, size: int, observed_satellites: dict = {}):
        self.position: Vector = position
        # TODO define max nav value with mass
        self.velocity: SatelliteVelocityHandler = SatelliteVelocityHandler(max_navigation_velocity_magnitude=10)
        self.__is_crashed: bool = False
        self.__observance_radius: int = 100
        self.__disturbance_duration = 0
        self.__mass = mass
        self.__size = size
        self.__observed_satellites: dict = observed_satellites
        self.__previously_observed_satellites: dict = {}
        self.__possible_collisions: dict = {}
        self.__disturbances: list = [Disturbance(), Disturbance(), Disturbance()]


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


    def possible_collisions(self) -> dict:
        return self.__possible_collisions


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
    def __str__(self):
        return f'{type(self)} center={self.center()}, velocity={self.velocity.value()}, radius={self.radius()}'


    def update_scale(self, scale_factor: float):
        self.__observance_radius *= scale_factor
        self.__size *= scale_factor
        self.position.set_vector(multiply(self.position, scalar=scale_factor))
        self.velocity.update_scale(scale_factor)
        self.update_arrow()

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
        self.update_arrow()

        self.position.add_to_x(self.velocity.value().x())
        self.position.add_to_y(self.velocity.value().y())


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


    def navigate_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        self.velocity.navigation_velocity().set_acceleration(0.5)
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


    def update_possible_collisions(self) -> dict:
        # TODO consider acceleration
        possible_collisions: dict = dict()
        satellite_trajectories = [self.__get_satellite_trajectory()]
        if self.velocity.value().magnitude() != 0:
            satellite_trajectories.extend(self.__get_parallel_trajectory(self.radius(), satellite_trajectories[0]))
        for observed_satellite in self.__observed_satellites:
            if observed_satellite in self.__previously_observed_satellites:
                previous_position: tuple = self.__previously_observed_satellites[observed_satellite]
                current_position: tuple = self.__observed_satellites[observed_satellite]
                observed_trajectory = StraightLineEquation(previous_position, current_position)
                possible_collisions[observed_satellite] = self.__analyse_given_object_system(
                    satellite_trajectories,
                    observed_trajectory,
                    observed_satellite)
        cleared_collisions = {
            key: value for key, value in possible_collisions.items() if value is not None}
        self.__possible_collisions = {k: v for k, v in
            sorted(cleared_collisions.items(), key=lambda item: item[1].time())}


    def avoid_possible_collisions(self):
        pass
        # first_collision = next(iter(self.__possible_collsions))


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __get_satellite_trajectory(self) -> StraightLineEquation:
        # TODO shift center to outer edge
        point1: Vector = self.center()
        point2: tuple = (self.velocity.value().x() + point1.x(), self.velocity.value().y() + point1.y())
        return StraightLineEquation(point1.get_as_tuple(), point2)


    def __get_parallel_trajectory(self, shift: float, trajectory: StraightLineEquation) -> tuple:
        velocity: Vector = Vector(trajectory.direction_vector[0], trajectory.direction_vector[1])

        # left turned
        left_tangent = velocity.tangent()
        left_turned_normalized_unit_vector: Vector = divide(left_tangent, left_tangent.magnitude())
        left_turned_normalized_vector: Vector = multiply(left_turned_normalized_unit_vector, shift)
        point2_left: tuple = (velocity.x() + left_turned_normalized_vector.x(),
        velocity.y() + left_turned_normalized_vector.y())
        left_trajectory = StraightLineEquation(left_turned_normalized_vector.get_as_tuple(), point2_left)

        # right turned
        right_tangent = multiply(left_tangent, -1)
        right_turned_normalized_unit_vector: Vector = divide(right_tangent, right_tangent.magnitude())
        right_turned_normalized_vector: Vector = multiply(right_turned_normalized_unit_vector, shift)
        point2_right: tuple = (velocity.x() + right_turned_normalized_vector.x(),
        velocity.y() + right_turned_normalized_vector.y())
        right_trajectory = StraightLineEquation(
            right_turned_normalized_vector.get_as_tuple(), point2_right)

        return left_trajectory, right_trajectory


    def __analyse_given_object_system(self,
            satellite_trajectories: list,
            observed_trajectory: StraightLineEquation,
            observed_object) -> Collision:
        """
        The given systems of two "moving" objects can be split up into 4 categories:
        1. both objects are moving
        2. object1 is moving, object2 is at rest
        3. object1 is at rest, object2 is moving
        4. both objects are at rest

        Parameters
        ----------
        satellite_trajectories : list[StraightLineEquation]
            trajectories  of the current satellite
        observed_trajectory : StraightLineEquation
            trajectory of the observed object

        Returns
        -------
        dict
            if a possible collision is detected it is added to the dict [oberved_object]=riskiest intersection
        """
        satellite_velocity = self.velocity.value().magnitude()
        observed_velocity = observed_trajectory.direction_vector_magnitude()
        if satellite_velocity == observed_velocity == 0:
            return None
        if satellite_velocity != 0 and observed_velocity == 0:
            return self.__check_collision_with_non_moving_object(satellite_trajectories, observed_object)

        observed_trajectories = [observed_trajectory]
        observed_trajectories.extend(self.__get_parallel_trajectory(
            observed_object.radius(), observed_trajectory))
        if satellite_velocity == 0 and observed_velocity != 0:
            return self.__check_collision_with_non_moving_object(observed_trajectories, observed_object,
                resting_satellite=True)
        if satellite_velocity != 0 and observed_velocity != 0:
            return self.__check_collision_with_moving_object(satellite_trajectories, observed_trajectories,
                observed_object)


    def __check_collision_with_non_moving_object(self, trajectories: list, other_object,
            resting_satellite=False) -> Collision:
        minimal_distance = self.radius() + other_object.radius()
        for trajectory in trajectories:
            if resting_satellite:
                center: tuple = self.center().get_as_tuple()
                dist = trajectory.distance_to_point(center)
            else:
                center: tuple = other_object.center().get_as_tuple()
                dist = trajectory.distance_to_point(center)
            if dist <= minimal_distance:
                # TODO has to be improved center is not first point of collision
                t = trajectory.plump_point(center)
                return Collision(other_object.center().get_as_tuple(), t)
        return None


    def __check_collision_with_moving_object(self, satellite_trajectories: list, observed_trajectories: list,
            observed_object) -> Collision:
        lgs = LinearSystemOfEquations()
        riskiest_collision: tuple = None
        nearest_hit = 1000  # a big number (far in the future)
        for observed_trajectory in observed_trajectories:
            for satellite_trajectory in satellite_trajectories:
                identical_trajectories: bool = lgs.check_identity(satellite_trajectory, observed_trajectory)
                if identical_trajectories:
                    t = lgs.calculate_moment_of_crash(satellite_trajectory, observed_trajectory)
                    intersection = satellite_trajectory.calculate_new_point(t)
                    is_risky = True
                else:
                    intersection: tuple = lgs.get_intersection(observed_trajectory, satellite_trajectory)
                    is_risky, t = self.__is_intersection_risky_and_when(intersection,
                        satellite_trajectory,
                        observed_trajectory,
                        observed_object)
                if is_risky and t < nearest_hit:
                    nearest_hit = t
                    riskiest_collision = intersection
        if riskiest_collision:
            return Collision(riskiest_collision, nearest_hit)
        return None


    def __is_intersection_risky_and_when(self,
            intersection: tuple,
            satellite_trajectory: StraightLineEquation,
            observed_trajectory: StraightLineEquation,
            observed_object) -> tuple:
        if intersection == (float('inf'), float('inf')):
            # TODO figure out what happend here
            return False, None
        observed_t: float = observed_trajectory.calculate_t(intersection)
        satellite_t: float = satellite_trajectory.calculate_t(intersection)
        satellite_at_observed_t: tuple = satellite_trajectory.calculate_new_point(observed_t)
        observed_satellite_at_satellite_t: tuple = observed_trajectory.calculate_new_point(satellite_t)
        distance = calculate_distance(tuple_to_vector(satellite_at_observed_t),
            tuple_to_vector(observed_satellite_at_satellite_t))
        t = min(satellite_t, observed_t)
        if distance <= (self.radius() + observed_object.radius()) and t >= 0:
            return True, t
        return False, t


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
