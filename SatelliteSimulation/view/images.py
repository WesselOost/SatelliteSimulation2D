# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Class Description
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import os
import pygame

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

SATELLITE = "satellite"
ONE = "1"
TWO = "2"
THREE = "3"
FOUR = "4"
CRASHED = "_crashed"
PNG = ".png"

BACKGROUND = "galaxy_background_1920_1080.png"
ASTEROID = "asteroid1.png"
EARTH = "earth.png"
DOTTED_CIRCLE = "dashed_circle.png"

ABSOLUTE_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_PATH = os.path.join(ABSOLUTE_ROOT_PATH, "Assets")


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Images:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self):
        filenames: list = [
            BACKGROUND,
            SATELLITE + ONE + PNG,
            SATELLITE + TWO + PNG,
            SATELLITE + THREE + PNG,
            SATELLITE + FOUR + PNG,
            SATELLITE + ONE + CRASHED + PNG,
            SATELLITE + TWO + CRASHED + PNG,
            SATELLITE + THREE + CRASHED + PNG,
            SATELLITE + FOUR + CRASHED + PNG,
            ASTEROID,
            EARTH,
            DOTTED_CIRCLE
        ]
        self.__images = {}
        for filename in filenames:
            self.__images[filename] = pygame.image.load(os.path.join(ASSETS_PATH, filename)).convert_alpha()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_satellite(self, satellite_type: int, is_crashed: bool):
        if is_crashed:
            return self.__images[SATELLITE + str(satellite_type) + CRASHED + PNG]

        return self.__images[SATELLITE + str(satellite_type) + PNG]


    def get_background(self):
        return self.__images[BACKGROUND]


    def get_asteroid(self):
        return self.__images[ASTEROID]


    def get_earth(self):
        return self.__images[EARTH]


    def get_dotted_circle(self):
        return self.__images[DOTTED_CIRCLE]


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def set_earth_size(self, earth_size: tuple):
        self.__images[EARTH] = pygame.transform.scale(self.__images[EARTH], earth_size)


    def set_background_size(self, border_size: tuple):
        self.__images[BACKGROUND] = pygame.transform.scale(self.__images[BACKGROUND], border_size)


# ----------------------------------------------------------------------- #
#  SUBSECTION: Private Methods
# ----------------------------------------------------------------------- #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


if __name__ == '__main__':
    pass
