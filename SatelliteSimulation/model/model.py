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
import time

from SatelliteSimulation.model.satellite import *
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
    def __init__(self, satelliteAmount: int,
                border_corner_x: int,
                border_corner_y: int,
                border_width: int,
                border_height: int,
                border_offset: int):
        ## public
        self.scale_factor: float = 1.0
        self.border_corner_x = border_corner_x
        self.border_corner_y = border_corner_y
        self.border_width = border_width
        self.border_height = border_height
        self.border_padding = border_offset
        self.satellites: list = self.__create_satellites(satelliteAmount)
        self.update_satellite_observance()
        ## __private


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    
        
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def update_satellite_observance(self):
        for satellite in self.satellites:
            satellite.visible_satellites = self.__get_visible_sattelites(satellite)
            satellite.check_satellite_status()
            
                
    def create_disturbance(self, disturbanceType: str):
        if disturbanceType == "MALFUNCTION":
            self.__create_malfunction()
        elif disturbanceType == "GRAVITY GRADIENT DISTURBANCE":
            self.__create_gavity_disturbance()
            print('damn gravity')
            pass
        elif disturbanceType == "SOLAR RADIATION DISTURBANCE":
            self.__create_radiation_disturbance()
            print('sun burn')
            pass
        elif disturbanceType == "MAGNETIC DISTURBANCE":
            self.__create_magnetic_disturbance()
            print('pls help Iron Man')
            pass


    def move_influenced_satellites(self)->bool:
        """
        If a satellite is disturbed by an external force
        or is malfunctioning and the duration of the forced 
        movement is greater 0 and its updating its position. 
        At the same time the duration is counted down. 
        If the satellite crossed a outer border it has to move
        one step backwards and to set the duration to zero.

        Returns
        -------
        bool
            True, if at least one satellite moved
        """
        has_moved = False
        temp_bool = False
        for satellite in self.satellites:
            if satellite.disturbance_duration > 0:
                satellite.x += satellite.velocity_x
                satellite.y += satellite.velocity_y
                satellite.disturbance_duration -= 1
                has_moved = True
                crahed_satellites = self.__check_crash_occurence(satellite)
                if crahed_satellites:
                    #TODO add conservation of momentum: p_ges = const = p1 + ... + pn = m1*v1+...+mn*vn
                    satellite.x -= satellite.velocity_x
                    satellite.y -= satellite.velocity_y
                    satellite.disturbance_duration = 0
                if not self.__inside_border(satellite, self.border_padding):
                    satellite.x -= satellite.velocity_x
                    satellite.y -= satellite.velocity_y
                    satellite.disturbance_duration = 0
                    if not temp_bool:
                        has_moved = False
            if satellite.disturbance_duration == 0:
                satellite.velocity_x = satellite.velocity_y = 0
            temp_bool = has_moved
        return has_moved
                
                
    def update_border_and_satellite_data(self,
                                        scale_factor,
                                        border_corner_x,
                                        border_corner_y,
                                        border_width,
                                        border_height,
                                        border_padding):
        self.scale_factor = scale_factor
        self.update_satellite_size_and_position(scale_factor)

        self.border_corner_x = border_corner_x
        self.border_corner_y = border_corner_y
        self.border_width = border_width
        self.border_height = border_height
        self.border_padding = border_padding


    def update_satellite_size_and_position(self, scale_factor: float):
        for satellite in self.satellites:
            satellite.observanceRadius *= scale_factor
            satellite.dangerZoneShift *= scale_factor
            satellite.dangerZoneRadius *= scale_factor
            satellite.size *= scale_factor
            satellite.x *= scale_factor
            satellite.y *= scale_factor
            if satellite.disturbance_duration > 0:
                satellite.velocity_x *= scale_factor
                satellite.velocity_y *= scale_factor


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __create_satellites(self, satelliteAmount: int) -> list:
        satellites = list()
        for satellite in range(satelliteAmount):
            while True:
                satellite = self.__create_random_satellite()
                if self.__no_overlapp(satellite, satellites) and self.__inside_border(satellite, self.border_padding):
                    satellites.append(satellite)
                    break
        return satellites
    
    
    def __check_crash_occurence(self, satellite:Satellite)->list:
        crashed_satellites = []
        for other_satellite in satellite.visible_satellites:
            outer_boarder = other_satellite.size/2 + satellite.size/2
            if calculate_distance(other_satellite.get_center(), satellite.get_center()) < outer_boarder*0.90:
                crashed_satellites.append(other_satellite)
        return crashed_satellites
    
    
    def __get_visible_sattelites(self, satellite: Satellite) -> list:
        visible_satellites = []
        for other_satellite in self.satellites:
            if other_satellite is not satellite:
                distance = calculate_distance(
                    other_satellite.get_center(), satellite.get_center())
                if distance <= satellite.observanceRadius:
                    visible_satellites.append(other_satellite)
        
        return visible_satellites


    def __create_random_satellite(self) -> Satellite:
        default_size = self.border_height // 10
        satellite_type = random.randint(1, SATELLITE_TYPE_AMOUNT)
        border_offset = self.border_padding
        position_x = random.randrange(self.border_corner_x + border_offset,
                                    self.border_corner_x + self.border_width - border_offset,
                                    border_offset)
        position_y = random.randrange(self.border_corner_y + border_offset,
                                    self.border_corner_y + self.border_height - border_offset,
                                    border_offset)
        if satellite_type == 1:
            return SatelliteA(position_x, position_y, math.ceil(default_size))
        if satellite_type == 2:
            return SatelliteB(position_x, position_y, math.ceil(default_size * 0.8))
        if satellite_type == 3:
            return SatelliteC(position_x, position_y, math.ceil(default_size * 1.2))
        if satellite_type == 4:
            return SatelliteD(position_x, position_y, math.ceil(default_size * 0.5))
        if satellite_type == 5:
            return SpaceJunk(position_x, position_y, math.ceil(default_size * 0.2))


    def __no_overlapp(self, new_satellite: Satellite, satellites: list) -> bool:
        if not satellites:
            return True
        # center coordinates for new satellite
        x1 = new_satellite.x + new_satellite.size / 2
        y1 = new_satellite.y + new_satellite.size / 2
        for satellite in satellites:

            # center coordinates of existing satellite
            x2 = satellite.x + satellite.size / 2
            y2 = satellite.y + satellite.size / 2

            distance = calculate_distance((x1, y1), (x2, y2))
            ref_distance = satellite.dangerZoneRadius + new_satellite.dangerZoneRadius
            if distance < ref_distance:
                return False
        return True


    def __inside_border(self, satellite: Satellite, offset: int) -> bool:
        right_valid_x = (satellite.x + satellite.size) < (self.border_corner_x + self.border_width - offset)
        left_valid_x = (self.border_corner_x + offset) < satellite.x
        top_valid_y = (self.border_corner_y + offset) < satellite.y
        bottom_valid_y = (satellite.y + satellite.size) < (self.border_corner_y + self.border_height - offset)
        if right_valid_x and left_valid_x and top_valid_y and bottom_valid_y:
            return True
        return False


    def __create_malfunction(self):
        try:
            malfunction = Disturbance()
            satellite = random.choice([satellite for satellite in self.satellites if not satellite.isCrashed])
            if satellite.disturbance_duration < malfunction.duration:
                satellite.disturbance_duration = malfunction.duration 
            satellite.velocity_x += malfunction.velocity_x * self.scale_factor
            satellite.velocity_y += malfunction.velocity_y * self.scale_factor
        except IndexError:
            #TODO everything is crashed, game over (maybe game over screen :p)
            pass
    
    
    def __create_gavity_disturbance(self):
        gravityDisturbance = Disturbance(120)
        for satellite in self.satellites:
            satellite.disturbance_duration = gravityDisturbance.duration
            satellite.velocity_y = gravityDisturbance.change_gravity(satellite.weight)
            
            
    def __create_radiation_disturbance(self):
        ref = self.border_height // 10 * 1.2
        radiation = Disturbance(ref**2)
        for satellite in self.satellites:
            satellite.disturbance_duration = radiation.duration
            satellite.velocity_x = radiation.velocity_x * radiation.add_radiation_pressure(
                satellite.surface)
            satellite.velocity_y = radiation.velocity_y * radiation.add_radiation_pressure(
                satellite.surface)
            
            
    def __create_magnetic_disturbance(self):
        magneticDisturbance = Disturbance(120)
        for satellite in self.satellites:
            satellite.disturbance_duration = magneticDisturbance.duration
            satellite.velocity_x = magneticDisturbance.velocity_x * magneticDisturbance.add_magnetic_disturbance(
                satellite.weight)
            satellite.velocity_y = magneticDisturbance.velocity_y * magneticDisturbance.add_magnetic_disturbance(
                satellite.weight)


class Disturbance:

    def __init__(self, reference_value:float=0):
        # duration in frames
        self.duration = random.randrange(60, 120, 1)

        # velocity vector in Pixel 
        self.velocity_x = random.uniform(-1, 1) * random.randint(0, 5)
        self.velocity_y = random.uniform(-1, 1) * random.randint(0, 5)
        
        self.reference_value = reference_value
        
        self.binary_direction = random.uniform(-1, 1)
        
    def change_gravity(self, mass:int)->float:
        # LAW: F_G = G * (M*m)/r^2, M>m
        # with G, m = const and r~const (because shift is to little)
        # => F_G = const * M
        # heavier objects should be more influenced by the force
        #TODO check if r is making a big difference
        return (mass/self.reference_value) * self.binary_direction
        
        
    def add_radiation_pressure(self, surface: int) -> float:
        # Radiation pressure from the sun
        if self.velocity_x != 0 and  self.velocity_y != -1:
            return (self.reference_value/surface) * 0.1
        self.velocity_x = random.uniform(-1, 1) * random.randint(0, 5)
        self.velocity_y = random.uniform(-1, 1) * random.randint(0, 5)
        return (surface/self.reference_value) * 0.1
    
    
    def add_magnetic_disturbance(self, mass: int) -> float:
        # assumption a satellite with more mass contains more metall
        # and more charge => is more attracted to the magnetic force 
        # of the earth
        #TODO compare the gravity/magnetic disturbance which is 
        return mass/self.reference_value * 0.3


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def calculate_distance(coord_A: tuple, coords_B: tuple) -> float:
    return math.sqrt((coords_B[0] - coord_A[0]) ** 2 + (coords_B[1] - coord_A[1]) ** 2)

def current_milli_time():
    return round(time.time() * 1000)


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    pass
