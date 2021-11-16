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
import os
import random
import math

from SatelliteSimulation.model.collision_handling import *
from SatelliteSimulation.model.satellite_border import SatelliteBorder
from SatelliteSimulation.model.disturbance.disturbance import *
from SatelliteSimulation.model.disturbance.disturbance_type import DisturbanceType
from SatelliteSimulation.model.satellite.satellite import *
from SatelliteSimulation.model.math.velocity import Velocity

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
        self.__border = border
        self.__satellites: list = self.__create_satellites(satellite_amount)
        self.__delta_time = 1

        self.update_satellite_observance()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def get_satellites(self) -> list:
        return self.__satellites


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
            Malfunction().apply_malfunction(self.__satellites, self.__scale_factor)
        elif disturbance_type == DisturbanceType.GRAVITATIONAL:
            GravitationalDisturbance(120).apply_disturbance(self.__satellites)
            print('damn gravity')
        elif disturbance_type == DisturbanceType.SOLAR_RADIATION:
            ref: float = self.__border.height() // 10 * 1.2
            SolarRadiationDisturbance(ref ** 2).apply_disturbance(self.__satellites)
            print('sun burn')
        elif disturbance_type == DisturbanceType.MAGNETIC:
            MagneticDisturbance(12).apply_disturbance(self.__satellites)
            print('pls help Iron Man')


    def move_satellites(self):
        for satellite in self.__satellites:
            satellite.move()
            if satellite.disturbance_duration() > 0:
                satellite.decrement_disturbance_duration()
                if satellite.disturbance_duration() <= 0:
                    # satellite.value.clear()
                    # TODO stop disturbance and decrement crashed satellites value
                    pass
            # if satellite.value.magnitude() < 0.1:
            #     satellite.value.clear()


    def check_and_handle_collisions(self):
        for index, satellite in enumerate(self.__satellites):
            # [index + 1] prevents checking previously compared satellites
            check_and_handle_satellite_collisions(satellite, self.__satellites[index + 1:])

            if not self.__border.is_object_inside_border(center=satellite.center(), radius=satellite.radius()):
                self.__handle_border_overlap(satellite)


    def update_satellite_observance(self):
        for satellite in self.__satellites:
            satellite.update_observed_satellites(self.__get_observed_satellites(satellite))


    def avoid_possible_future_collisions(self):
        for satellite in self.__satellites:
            if not satellite.is_crashed():
                possible_collisions: dict = satellite.detect_possible_collisions(satellite.previously_observed_satellites())
                if possible_collisions:
                    print(possible_collisions)
                satellite.avoid_possible_collisions(possible_collisions)


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
        x = random.randrange(border.left(), border.right(), 1)
        y = random.randrange(border.top(), border.bottom(), 1)
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
                if distance <= observing_satellite.observance_radius():
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
            minimal_distance = satellite.radius() + satellite.observance_radius() + \
                               new_satellite.radius() + new_satellite.observance_radius()
            if distance < minimal_distance:
                return False
        return True


    def __handle_border_overlap(self, satellite: Satellite):
        border: SatelliteBorder = self.__border
        satellite_x = satellite.position.x()
        satellite_size = satellite.size()
        satellite_right_edge = satellite_x + satellite_size

        if satellite_right_edge > border.right():
            satellite.position.set_x(border.right() - satellite_size)

        if satellite_x < border.left():
            satellite.position.set_x(border.left())

        satellite_y = satellite.position.y()
        satellite_bottom_edge = satellite_y + satellite_size

        if satellite_y < border.top():
            satellite.position.set_y(border.top())

        if satellite_bottom_edge > border.bottom():
            satellite.position.set_y(border.bottom() - satellite_size)
        satellite.velocity.disturbance_velocity().clear()
        satellite.velocity.navigation_velocity().clear()
        satellite.velocity.collision_velocity().clear()


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
