#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Link    : link
# @Version : 0.0.1
"""
Short Introduction
"""

# =========================================================================== #
#  SECTION: Imports                                                           
# =========================================================================== #
import os
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
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
        self.dangerZoneRadius: int = None
        self.x = x
        self.y = y
        self.weigth = weigth
        self.suface = width * height
        self.radius = max(width, height)
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
    def __init__(self, satelliteAmount: int):
        ## public
        self.satellites: list = self.__create_satellites(satelliteAmount)
        ## __private

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def create_disturbance(self, disturbanceType: str):
        pass


    def detect_possible_collision(self):
        pass

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __create_satellites(self, satelliteAmount: int):
        pass


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #

if __name__ == '__main__':
    pass
