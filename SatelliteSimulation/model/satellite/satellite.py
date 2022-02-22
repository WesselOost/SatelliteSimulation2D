"""
Satellite and Satellite sub classes
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import random
from abc import ABC

from model.basic_math.math_basic import *
from model.basic_math.motion import FutureCollisionDetector, Trajectory, direction_changed
from model.basic_math.vector import *
from model.collision.future_collision_data import FutureCollisionData
from model.collision.collision_avoidance_handler import \
    calculate_degrees_which_avoids_object_by_90_degrees
from model.disturbance.disturbance import Disturbance
from model.satellite.satellite_velocity_handler import SatelliteVelocityHandler


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
        self.velocity_handler: SatelliteVelocityHandler = SatelliteVelocityHandler(max_navigation_velocity_magnitude=4)
        self.__observance_radius: float = 100
        self.__is_crashed: bool = False
        self.__mass = mass
        self.__size = size
        self.__observed_satellites: dict = observed_satellites
        self.__possible_collisions: dict = {}
        self.__disturbances: list = []
        self.__previous_four_positions: list = [self.position] * 4


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def observance_radius(self):
        return self.__observance_radius

    @observance_radius.setter
    def obervance_radius(self, new_radius: float):
        self.__observance_radius = min(200, max(new_radius, 0))
        
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
        return f'{self.__class__.__name__} id={self.satellite_id} center={self.center()}, velocity={self.velocity_handler.velocity()}, radius={self.radius()}'


    def update_crashed_status(self):
        if not self.__is_crashed:
            self.__is_crashed = True
            self.velocity_handler.navigation_velocity().clear()


    def update_observed_satellites(self, new_observed_satellites: dict):
        self.__observed_satellites = new_observed_satellites


    def move(self):
        self.velocity_handler.update_velocities(self.__disturbances)
        self.__disturbances = [disturbance for disturbance in self.__disturbances if disturbance.velocity().t() > 0]

        self.position.add_to_x(self.velocity_handler.velocity().x())
        self.position.add_to_y(self.velocity_handler.velocity().y())
        self.__update_previous_four_position()


    def navigate_to_in_degree(self, direction_in_degrees: int):
        """
                  north 90
        west 180          east 0 (360)
                 south 270

        :param direction_in_degrees:
        :return:
        """
        angle_in_radians = np.math.radians(direction_in_degrees)
        max_nav_velocity = self.velocity_handler.max_navigation_velocity()
        x = max_nav_velocity * np.math.cos(angle_in_radians)
        y = max_nav_velocity * np.math.sin(angle_in_radians)
        self.velocity_handler.set_navigation_velocity(Vector(x, y))
        self.velocity_handler.navigation_velocity().solve_equation_and_set_v1_v2(self.velocity_handler.max_navigation_velocity(), 20)


    def manually_steer_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        self.velocity_handler.navigation_velocity().solve_equation_and_set_v1_v2(self.velocity_handler.max_navigation_velocity(), 20)
        nav_x: float = self.velocity_handler.navigation_velocity().x()
        nav_y: float = self.velocity_handler.navigation_velocity().y()

        if pressed_left:
            self.velocity_handler.set_navigation_velocity(Vector(-1, nav_y))
        if pressed_up:
            self.velocity_handler.set_navigation_velocity(Vector(nav_x, -1))
        if pressed_right:
            self.velocity_handler.set_navigation_velocity(Vector(1, nav_y))
        if pressed_down:
            self.velocity_handler.set_navigation_velocity(Vector(nav_x, 1))


    def update_possible_collisions(self):
        possible_collisions: dict = {}
        for observed_satellite in self.__observed_satellites:
            recorded_positions: list = self.__observed_satellites[observed_satellite]
            if self.__list_length_valid_and_at_least_one_sat_moving(recorded_positions, 4):
                if direction_changed(recorded_positions):
                    recorded_positions = recorded_positions[-2:]
                    self.__observed_satellites[observed_satellite] = recorded_positions
                recorded_positions.reverse()
                observed_trajectory: Trajectory = Trajectory(recorded_positions)
                satellite_trajectory: Trajectory = Trajectory(
                    [self.center().get_as_tuple()] * 4)
                if self.velocity_handler.velocity().magnitude() != 0:
                    previous_positions = [p.get_as_tuple() for p in self.__previous_four_positions]
                    previous_positions.reverse()
                    satellite_trajectory: Trajectory = Trajectory(previous_positions)
                collision: FutureCollisionData = FutureCollisionDetector(
                    self.radius(), observed_satellite.radius(),
                    observed_trajectory, satellite_trajectory).is_collision_possible()
                if collision:
                    possible_collisions[observed_satellite] = collision
        self.__possible_collisions = {k: v for k, v in
                                      sorted(possible_collisions.items(), key=lambda item: item[1].time())}


    def avoid_possible_collisions(self):
        observed_satellite = list(self.__possible_collisions)[0]
        observed_trajectory: Trajectory = self.__possible_collisions[observed_satellite].trajectory
        self.navigate_to_in_degree(
            calculate_degrees_which_avoids_object_by_90_degrees(observed_trajectory.get_direction_vector(),
                                                                observed_trajectory.get_current_position(),
                                                                self.velocity_handler.velocity(),
                                                                self.center()))



    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __update_previous_four_position(self):
        self.__previous_four_positions.insert(0, self.center())
        self.__previous_four_positions = self.__previous_four_positions[:4]


    def __list_length_valid_and_at_least_one_sat_moving(self, positions: list, min_list_length=4) -> bool:
        list_length_is_valid: bool = len(positions) >= max(2, min_list_length)
        if not list_length_is_valid:
            return False
        # if none are moving
        return not (positions[-1] == positions[-2] and not self.velocity_handler.velocity().magnitude())



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


