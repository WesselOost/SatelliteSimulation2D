#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : https://de.wikipedia.org/wiki/Bahnst%C3%B6rung#Schwerefeldvariationen
# @Version : 0.0.1
"""
The model of the satellite simulation. All the data is stored in that class.
The used velocities are assumed to be constant during the movement. 
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import copy
import logging
import os
import math

from SatelliteSimulation.model.collision_handling import *
from SatelliteSimulation.model.satellite_border import SatelliteBorder
from SatelliteSimulation.model.disturbance.disturbance import *
from SatelliteSimulation.model.disturbance.disturbance_type import DisturbanceType
from SatelliteSimulation.model.satellite.satellite import *

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
SATELLITE_TYPE_AMOUNT = 5


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Space:
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, satellite_amount: int, border: SatelliteBorder):
        self.__scale_factor: float = 1.0
        self.__border: SatelliteBorder = border
        self.__satellites: list = self.__create_satellites(satellite_amount)
        self.__delta_time = 1

        self.update_satellite_observance()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def get_satellites(self) -> list:
        return self.__satellites


    def get_border(self) -> SatelliteBorder:
        return self.__border


    def delta_time(self) -> float:
        return self.__delta_time


    def set_delta_time(self, delta_time):
        self.__delta_time = delta_time


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def update_border_and_satellite_scale(self, scale_factor):
        self.__scale_factor = scale_factor
        for satellite in self.__satellites:
            satellite.update_scale(scale_factor)

        self.__border.update_scale(scale_factor)


    def create_disturbance(self, disturbance_type: DisturbanceType):

        if disturbance_type == DisturbanceType.MALFUNCTION:
            satellite = random.choice([satellite for satellite in self.__satellites if not satellite.is_crashed()])
            satellite.append_disturbance(Malfunction(self.__scale_factor))
        elif disturbance_type == DisturbanceType.SOLAR_RADIATION:
            # TODO check max surface
            max_surface: float = (self.__border.height() // 10 * 1.2) ** 2
            disturbance = SolarRadiationDisturbance(max_surface, self.__scale_factor)
            for satellite in self.__satellites:
                self.append_disturbance_to_satellite(disturbance, satellite, satellite.surface())
            logging.info('sun burn')
        elif disturbance_type == DisturbanceType.GRAVITATIONAL:
            disturbance = GravitationalDisturbance(max_mass=120, scale_factor=self.__scale_factor)
            for satellite in self.__satellites:
                self.append_disturbance_to_satellite(disturbance, satellite, satellite.mass())
            logging.info('damn gravity')

        elif disturbance_type == DisturbanceType.MAGNETIC:
            disturbance = MagneticDisturbance(max_mass=120, scale_factor=self.__scale_factor)
            for satellite in self.__satellites:
                self.append_disturbance_to_satellite(disturbance, satellite, satellite.mass())
            logging.info('pls help Iron Man')


    def append_disturbance_to_satellite(self, disturbance, satellite, influence_attribute):
        disturbance_copy = copy.deepcopy(disturbance)
        disturbance_copy.update_trajectory(influence_attribute)
        satellite.append_disturbance(disturbance_copy)


    def move_satellites(self):
        for satellite in self.__satellites:
            satellite.move(self.__delta_time)


    def check_and_handle_collisions(self):
        for index, satellite in enumerate(self.__satellites):
            # [index + 1] prevents checking previously compared satellites
            check_and_handle_satellite_collisions(satellite, self.__satellites[index + 1:])
        a_satellite_out_of_border = True
        satellite_overlap = True
        while a_satellite_out_of_border and satellite_overlap:
            satellite_overlap = False
            a_satellite_out_of_border = False
            for satellite in self.__satellites:
                if not self.__border.is_object_inside_border(center=satellite.center(), radius=satellite.radius()):
                    a_satellite_out_of_border = True
                    x_shift, y_shift = self.__handle_border_overlap(satellite)
                    satellite_overlap = satellites_overlap or self.handle_satellite_overlap_shifts(x_shift, y_shift)


    def handle_satellite_overlap_shifts(self, x_shift, y_shift) -> bool:
        overlap_occurred: bool = False
        for i, sat1 in enumerate(self.__satellites):
            for sat2 in self.__satellites[i + 1:]:

                if satellites_overlap(sat1, sat2):
                    overlap_occurred = True
                    self.shift_x(sat1, sat2, x_shift)
                    self.shift_y(sat1, sat2, y_shift)

        return overlap_occurred


    def shift_x(self, sat1: Satellite, sat2: Satellite, x_shift: float):
        x1 = sat1.position.x()
        x2 = sat2.position.x()
        if self.no_shift_or_positions_equal(x1, x2, x_shift):
            pass
        elif self.p1_further_from_border_than_p2(x1, x2, x_shift):
            sat1.position.add_to_x(x_shift)
        else:
            sat2.position.add_to_x(x_shift)


    def shift_y(self, sat1: Satellite, sat2: Satellite, y_shift: float):
        y1 = sat1.position.y()
        y2 = sat2.position.y()
        if self.no_shift_or_positions_equal(y1, y2, y_shift):
            pass
        elif self.p1_further_from_border_than_p2(y1, y2, y_shift):
            sat1.position.add_to_y(y_shift)
        else:
            sat2.position.add_to_y(y_shift)


    def no_shift_or_positions_equal(self, p1, p2, shift):
        return shift == 0 or p1 == p2


    def p1_further_from_border_than_p2(self, p1: float, p2: float, shift: float) -> bool:
        return (shift > 0 and p1 > p2) or (shift < 0 and p1 < p2)


    def update_satellite_observance(self):
        for satellite in self.__satellites:
            satellite.update_observed_satellites(self.__get_observed_satellites(satellite))


    def avoid_possible_future_collisions(self):
        for satellite in self.__satellites:
            if not satellite.is_crashed():
                satellite.update_possible_collisions()

                if satellite.possible_collisions():
                    for possible_collision in satellite.possible_collisions():
                        logging.debug(possible_collision)
                        satellite.avoid_possible_collisions()


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
        return satellites


    def __create_random_satellite(self) -> Satellite:
        border: SatelliteBorder = self.__border
        default_size: float = border.height() // 10
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


    def __get_observed_satellites(self, observing_satellite: Satellite) -> dict:
        observed_satellites = {}
        for satellite in self.__satellites:
            if satellite is not observing_satellite:
                distance = calculate_distance(satellite.center(), observing_satellite.center())
                if distance - satellite.radius() <= observing_satellite.radius() + observing_satellite.observance_radius():
                    observed_satellites[satellite] = satellite.center().get_as_tuple()
                else:
                    # remove unobserved satellite from dict
                    observed_satellites.pop(satellite, None)
        return observed_satellites


    def __no_observance_radius_overlap(self, new_satellite: Satellite, satellites: list) -> bool:
        if not satellites:
            return True

        for satellite in satellites:
            distance: float = calculate_distance(new_satellite.center(), satellite.center())
            minimal_distance = satellite.radius() + satellite.observance_radius() + new_satellite.radius() + new_satellite.observance_radius()
            if distance < minimal_distance:
                return False
        return True


    def __handle_border_overlap(self, satellite: Satellite) -> tuple:
        border: SatelliteBorder = self.__border
        satellite_x = satellite.position.x()
        satellite_size = satellite.size()
        satellite_right_edge = satellite_x + satellite_size

        new_x: float = satellite_x

        if satellite_right_edge > border.right():
            new_x = border.right() - satellite_size

        if satellite_x < border.left():
            new_x = border.left()

        satellite.position.set_x(new_x)

        satellite_y = satellite.position.y()
        satellite_bottom_edge = satellite_y + satellite_size
        new_y: float = satellite_y

        if satellite_y < border.top():
            new_y = border.top()

        if satellite_bottom_edge > border.bottom():
            new_y = border.bottom() - satellite_size

        satellite.position.set_y(new_y)
        satellite.velocity.disturbance_velocity().clear()
        satellite.velocity.navigation_velocity().clear()
        satellite.velocity.collision_velocity().clear()

        return new_x - satellite_x, new_y - satellite_y


    def navigate_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        satellite = self.__satellites[0]
        satellite.navigate_satellite(pressed_left, pressed_up, pressed_right, pressed_down)

        # =========================================================================== #
        #  SECTION: Function definitions
        # =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    pass
