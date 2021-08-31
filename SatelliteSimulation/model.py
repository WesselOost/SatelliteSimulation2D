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
import threading
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
    def __init__(self, x: int, y: int, weigth: int, width: int, height: int, imgUrl: str):
        ## public
        self.isCrashed: bool = False
        self.observanceRadius: int = None
        self.dangerZoneShift: int = 20
        self.x = x
        self.y = y
        self.weigth = weigth
        self.suface = width * height
        self.size = max(width, height)
        self.dangerZoneRadius = self.size//2 + self.dangerZoneShift
        self.imgUrl = imgUrl
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
    def __init__(self, x: int, y: int):
        super().__init__(x,
                         y,
                         weigth=100,
                         width=50,
                         height=50,
                         imgUrl=os.path.join(ABSOLUTE_PATH, "Assets", "satellite1.png"))


class SatelliteB(Satellite):
    def __init__(self, x: int, y: int):
        super().__init__(x,
                         y,
                         weigth=80,
                         width=40,
                         height=40,
                         imgUrl=os.path.join(ABSOLUTE_PATH, "Assets", "satellite2.png"))


class SatelliteC(Satellite):
    def __init__(self, x: int, y: int):
        super().__init__(x,
                         y,
                         weigth=120,
                         width=60,
                         height=60,
                         imgUrl=os.path.join(ABSOLUTE_PATH, "Assets", "satellite3.png"))


class Space:
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, satelliteAmount: int,
                 border_corner_x: int = 0,
                 border_corner_y: int = 0,
                 border_width: int = 800,
                 border_heigth: int = 400):
        ## public
        self.border_corner_x = border_corner_x
        self.border_corner_y = border_corner_y
        self.border_width = border_width
        self.border_height = border_heigth
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
            disturbance = threading.Thread(target=self.__create_malfunction, args=(self.satellites,))
            
        disturbance.start()


    def detect_possible_collision(self):
        pass

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __create_satellites(self, satelliteAmount: int)->list:
        satellites = list()
        for satellite in range(satelliteAmount):
            while True:
                satellite = self.__create_random_satellite()
                if self.__no_overlapp(satellite, satellites) and self.__inside_border(satellite):
                    satellites.append(satellite)
                    break
        return satellites
                

    def __create_random_satellite(self) -> Satellite:
        satellite_type = random.randint(1,SATELLITE_TYPE_AMOUNT)
        position_x = random.randrange(self.border_corner_x + 10,
                                      self.border_corner_x + self.border_width -10,
                                      10)
        position_y = random.randrange(self.border_corner_y + 10 ,
                                      self.border_corner_y + self.border_height -10,
                                      10)
        if satellite_type == 1:
            return SatelliteA(position_x, position_y)
        if satellite_type == 2:
            return SatelliteB(position_x, position_y)
        if satellite_type == 3:
            return SatelliteC(position_x, position_y)

    
    def __no_overlapp(self, new_satellite:Satellite, satellites:list) -> bool:
        if not satellites:
            return True
        #center coordinates for new satellite
        x1 = new_satellite.x + new_satellite.size//2
        y1 = new_satellite.y + new_satellite.size//2
        for satellite in satellites:
            #center coordinates of existing satellite
            x2 = satellite.x + satellite.size//2
            y2 = satellite.y + satellite.size//2

            distance = calculate_distance((x1,y1),(x2,y2))
            ref_distance = satellite.dangerZoneRadius + new_satellite.dangerZoneRadius
            if distance < ref_distance:
                return False
        return True


    def __inside_border(self, satellite:Satellite, offset:int = 10)->bool:
        valid_x = self.border_corner_x + offset < (satellite.x + satellite.size) < (self.border_corner_x + self.border_width - offset)
        valid_y = self.border_corner_x + offset <(satellite.y + satellite.size) < (self.border_corner_y + self.border_height - offset)
        if valid_x and valid_y:
            return True
        return False


    def __create_malfunction(self, satellites:list):
        satellite = satellites[random.randint(0,len(satellites)-1)]
        x = satellite.x
        y = satellite.y
        duration = random.randrange(100,3000,10) #ms
        #disturbance direction in radians
        disturbance_direction = math.radians(random.randint(1,360))
        x_shift = math.sin(disturbance_direction)
        y_shift = math.cos(disturbance_direction)
        #velocity in Pixel per ms
        velocity = random.randint(10,100)/1000
        begin = current_milli_time()
        t = 0
        while duration >= t:
            old_x = satellite.x
            old_y = satellite.y
            satellite.x = x + x_shift * velocity * t
            satellite.y = y + y_shift * velocity * t
            if not self.__inside_border(satellite):
                satellite.x = old_x
                satellite.y = old_y
                break
            t = current_milli_time() - begin
            
# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def calculate_distance(coord_A:tuple, coords_B:tuple)->float:
    return math.sqrt((coords_B[0]-coord_A[0])**2 + (coords_B[1]-coord_A[1])**2)


def current_milli_time():
    return round(time.time() * 1000)



# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    pass
