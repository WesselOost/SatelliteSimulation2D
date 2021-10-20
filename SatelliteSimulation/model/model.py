#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Link    : link
# @Version : 0.0.1
"""
The model of the satellite simulation. All the data is stored in that class.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import os
import random
import math
import time

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
SATELLITE_TYPE_AMOUNT = 3


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Satellite:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: int, y: int, weight: int, size: int):
        ## public
        self.isCrashed: bool = False
        self.observanceRadius: int = None
        self.dangerZoneShift: int = 20
        self.x = x
        self.y = y
        self.malfunction_duration = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.weight = weight
        self.surface = size * size
        self.size = size
        self.dangerZoneRadius = self.size // 2 + self.dangerZoneShift
        ## __private


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def moveTo(self, new_x: int, new_y: int):
        pass


    def initiate_crash(self):
        pass

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


class SatelliteA(Satellite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x,
                         y,
                         weight=100,
                         size=size)


class SatelliteB(Satellite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x,
                         y,
                         weight=80,
                         size=size)


class SatelliteC(Satellite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x,
                         y,
                         weight=120,
                         size=size)


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
        ## __private


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def create_disturbance(self, disturbanceType: str):
        if disturbanceType == "MALFUNCTION":
            # disturbance = threading.Thread(target=self.__create_malfunction, args=(self.satellites,))
            # disturbance.start()
            self.__create_malfunction2()


    def detect_possible_collision(self):
        pass


    def move_malfunctioning_satellites(self):
        for satellite in self.satellites:
            if satellite.malfunction_duration > 0:
                satellite.x += satellite.velocity_x
                satellite.y += satellite.velocity_y
                satellite.malfunction_duration -= 1
                if not self.__inside_border(satellite, self.border_padding):
                    satellite.x -= satellite.velocity_x
                    satellite.y -= satellite.velocity_y
                    satellite.malfunction_duration = 0


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


    def __create_malfunction(self, satellites: list, degub: bool = True):
        satellite = satellites[random.randint(0, len(satellites) - 1)]
        start_x = satellite.x
        start_y = satellite.y

        malfunction = Disturbance()
        duration = malfunction.duration
        direction = malfunction.direction
        velocity = malfunction.velocity

        if degub:
            print(
                f"MALFUNCTION: {duration} ms; direction={360 - math.degrees(direction):.2f}; velocity={velocity * 1000} Pixel/s")
        self.__move_satellite(start_x, start_y, duration, velocity, direction, satellite)


    def __create_malfunction2(self):
        satellite = self.satellites[random.randint(0, len(self.satellites) - 1)]
        satellite.malfunction_duration = Disturbance().duration2
        satellite.velocity_x = Disturbance().velocity_x * self.scale_factor
        satellite.velocity_y = Disturbance().velocity_y * self.scale_factor


    def __move_satellite(self, start_x: int, start_y: int, duration: int, velocity: int, direction: int,
                         satellite: Satellite):
        x_shift = math.sin(direction)
        y_shift = math.cos(direction)
        begin = current_milli_time()
        t = 0
        while duration >= t:
            old_x = satellite.x
            old_y = satellite.y
            satellite.x = start_x + x_shift * velocity * t
            satellite.y = start_y + y_shift * velocity * t
            if not self.__inside_border(satellite, self.border_padding):
                satellite.x = old_x
                satellite.y = old_y
                break
            t = current_milli_time() - begin


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
            satellite.size *= scale_factor
            satellite.x *= scale_factor
            satellite.y *= scale_factor
            if satellite.malfunction_duration > 0:
                satellite.velocity_x *= scale_factor
                satellite.velocity_y *= scale_factor


class Disturbance:

    def __init__(self):
        # duration in ms
        self.duration = random.randrange(100, 3000, 10)
        self.duration2 = random.randrange(60, 120, 1)

        # disturbance direction in radians
        self.direction = math.radians(random.randint(1, 360))

        # velocity in Pixel per ms
        self.velocity = random.randint(10, 100) / 1000
        self.velocity_x = random.uniform(-1, 1) * random.randint(1, 5)
        self.velocity_y = random.uniform(-1, 1) * random.randint(1, 5)


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
