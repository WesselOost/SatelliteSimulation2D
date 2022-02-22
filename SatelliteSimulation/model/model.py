# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import copy
import os
from types import new_class
import pandas as pd

from model.arrow import Arrow
from model.border import Border
from model.collision.collision_handler import check_and_handle_satellite_collisions, \
    check_and_handle_border_collisions
from model.disturbance.disturbance import *
from model.disturbance.disturbance_type import DisturbanceType
from model.satellite.satellite import *

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
SATELLITE_TYPE_AMOUNT = 5


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #

class Space:
    """
    The model of the satellite simulation.
    The used velocities are assumed to be constant during the movement.
    """
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, satellite_amount: int, border: Border, config_data: pd.DataFrame = None):
        self._config_data: pd.DataFrame = config_data
        self.__border: Border = border
        self.__satellites: list = self.__create_satellites(satellite_amount)
        self.__delta_time = 1
        self.update_satellite_observance()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def config_data(self):
        return self._config_data

    def get_satellites(self) -> list:
        return self.__satellites


    def get_border(self) -> Border:
        return self.__border


    def delta_time(self) -> float:
        return self.__delta_time


    def set_delta_time(self, delta_time):
        self.__delta_time = delta_time


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def create_disturbance(self, disturbance_type: DisturbanceType):
        if disturbance_type == DisturbanceType.MALFUNCTION:
            not_crashed_satellites = [satellite for satellite in self.__satellites if not satellite.is_crashed()]
            if not_crashed_satellites:
                satellite = random.choice(not_crashed_satellites)
                satellite.append_disturbance(Malfunction())
        elif disturbance_type == DisturbanceType.SOLAR_RADIATION:
            max_surface: float = (self.__border.height() // 10 * 1.2) ** 2
            disturbance = SolarRadiationDisturbance(max_surface)
            for satellite in self.__satellites:
                append_disturbance_to_satellite(disturbance, satellite, satellite.surface())
        elif disturbance_type == DisturbanceType.GRAVITATIONAL:
            disturbance = GravitationalDisturbance(max_mass=120)
            for satellite in self.__satellites:
                append_disturbance_to_satellite(disturbance, satellite, satellite.mass())
        elif disturbance_type == DisturbanceType.MAGNETIC:
            disturbance = MagneticDisturbance(max_mass=120)
            for satellite in self.__satellites:
                append_disturbance_to_satellite(disturbance, satellite, satellite.mass())


    def move_satellites(self):
        for satellite in self.__satellites:
            satellite.move()


    def get_velocity_arrows(self) -> list:
        return list(map(satellite_to_magnitude_arrow, [satellite for satellite in self.__satellites
                                                       if satellite.velocity_handler.velocity().magnitude() != 0]))


    def check_and_handle_collisions(self):
        for index, satellite in enumerate(self.__satellites):
            # [index + 1] prevents checking previously compared satellites
            check_and_handle_satellite_collisions(satellite, self.__satellites[index + 1:])

        check_and_handle_border_collisions(self.__border, self.__satellites)


    def update_satellite_observance(self):
        for satellite in self.__satellites:
            observed_satellites = self.__get_observed_satellites(satellite)
            previous_observed_satellites = satellite.observed_satellites()
            # clean old observance
            observance_dict = {
                k: previous_observed_satellites[k] for k in observed_satellites if k in previous_observed_satellites}
            # update and adding new
            for observed_satellite in observed_satellites:
                if observed_satellite in observance_dict:
                    observance_dict[observed_satellite].insert(0, observed_satellite.center().get_as_tuple())
                    limit = min(len(observance_dict[observed_satellite]), 4)
                    observance_dict[observed_satellite] = observance_dict[observed_satellite][:limit]
                else:
                    observance_dict[observed_satellite] = [
                        observed_satellite.center().get_as_tuple()]
            satellite.update_observed_satellites(observance_dict)


    def avoid_possible_future_collisions(self):
        for satellite in self.__satellites:
            if not satellite.is_crashed():
                satellite.update_possible_collisions()

                if satellite.possible_collisions():
                    satellite.avoid_possible_collisions()


    def manually_steer_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        satellite = self.__satellites[0]
        satellite.manually_steer_satellite(pressed_left, pressed_up, pressed_right, pressed_down)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __create_satellites(self, satelliteAmount: int) -> list:
        satellites = list()
        for satellite in range(satelliteAmount):
            while True:
                satellite = self.__create_random_satellite()

                inside_border = self.__border.is_object_inside_border(satellite.center(), satellite.radius())
                if self.__no_observance_radius_overlap(satellite, satellites) and inside_border:
                    satellites.append(satellite)
                    break
        if self.config_data is not None:
            _ = [self. __update_config_observance_radius(satellite) for satellite in satellites]
        return satellites


    def __create_random_satellite(self) -> Satellite:
        border: Border = self.__border
        default_size: float = border.height() // 14
        satellite_type: int = random.randint(1, SATELLITE_TYPE_AMOUNT)
        x = random.randrange(int(border.left()), int(border.right()), 1)
        y = random.randrange(int(border.top()), int(border.bottom()), 1)
        position: Vector = Vector(x, y)

        if satellite_type == 1:
            return SatelliteA(position, math.ceil(default_size))
        elif satellite_type == 2:
            return SatelliteB(position, math.ceil(default_size * 0.8))
        elif satellite_type == 3:
            return SatelliteC(position, math.ceil(default_size * 1.2))
        elif satellite_type == 4:
            return SatelliteD(position, math.ceil(default_size * 0.6))
        elif satellite_type == 5:
            return SpaceJunk(position, math.ceil(default_size * 0.2))


    def __no_observance_radius_overlap(self, new_satellite: Satellite, satellites: list) -> bool:
        if not satellites:
            return True

        for satellite in satellites:
            distance: float = calculate_distance(new_satellite.center(), satellite.center())
            minimal_distance = satellite.radius() + satellite.observance_radius + new_satellite.radius() + new_satellite.observance_radius
            if distance < minimal_distance:
                return False
        return True
    
    def __update_config_observance_radius(self, satellite: Satellite) -> None:
        satellite_type: str = satellite.__class__.__name__
        new_radius = 100
        if satellite_type in list(self.config_data) and np.issubdtype(self.config_data[satellite_type].dtype, np.number):
            new_radius = float(self.config_data.loc['observance-radius [0-300]', satellite_type])
        satellite.observance_radius = new_radius

    def __get_observed_satellites(self, observing_satellite: Satellite) -> list:
        observed_satellites = []
        for satellite in self.__satellites:
            if satellite is not observing_satellite:
                distance = calculate_distance(satellite.center(), observing_satellite.center())
                if distance - satellite.radius() <= observing_satellite.radius() + observing_satellite.observance_radius:
                    observed_satellites.append(satellite)
        return observed_satellites


        # =========================================================================== #
        #  SECTION: Function definitions
        # =========================================================================== #


def append_disturbance_to_satellite(disturbance, satellite, influence_attribute):
    disturbance_copy = copy.deepcopy(disturbance)
    disturbance_copy.update_trajectory(influence_attribute)
    satellite.append_disturbance(disturbance_copy)


def satellite_to_magnitude_arrow(satellite: Satellite) -> Arrow:
    magnitude: float = satellite.velocity_handler.velocity().magnitude()
    unit_normal: Vector = satellite.velocity_handler.velocity().unit_normal()
    radius: float = satellite.radius()
    center: Vector = satellite.center()

    start_vector: Vector = Vector(center.x() + radius * unit_normal.x(), center.y() + radius * unit_normal.y())
    unit_normal_direction_vector: Vector = add(start_vector, unit_normal)

    return Arrow(start_vector, unit_normal_direction_vector, magnitude)


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

