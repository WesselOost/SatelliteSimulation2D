# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
An earth Icon that rotates with a dotted outline around it
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import os
import pygame

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EARTH_IMG = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "earth.png"))
DOTTED_CIRCLE = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "dashed_circle.png"))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Earth:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, surface: pygame.Surface, dotted_circle_offset: float, scale_factor: float):
        EARTH_IMG.convert()
        DOTTED_CIRCLE.convert()
        self.__surface = surface
        self.__center_x = x
        self.__dotted_circle_offset = dotted_circle_offset
        self.__earth_img_angle = 0
        self.__earth_scale = 0.4 * scale_factor
        self.__set_dotted_circle_size_and_position()
        # position
        self.__dotted_circle_position = \
            (self.__center_x - self.__dotted_circle.get_width() // 2), \
                self.__surface.get_height() - self.__dotted_circle.get_height() // 2


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def draw(self):
        self.__surface.blit(self.__dotted_circle, self.__dotted_circle_position)
        self.__rotate_and_draw_earth()


    def get_dotted_circle_position(self) -> tuple:
        return self.__dotted_circle_position[0], self.__dotted_circle_position[1]


    def get_dotted_circle_width(self) -> int:
        return self.__dotted_circle.get_width()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def on_size_changed(self, surface: pygame.Surface, scale_factor: float):
        self.__surface = surface
        self.__earth_scale *= scale_factor
        self.__center_x *= scale_factor
        self.__dotted_circle_offset *= scale_factor
        self.__dotted_circle_position = self.__dotted_circle_position[0] * scale_factor, \
            self.__dotted_circle_position[1] * scale_factor
        self.__set_dotted_circle_size_and_position()


    def __rotate_and_draw_earth(self):
        self.__earth_img_angle -= 0.2
        earth_img_rotated = pygame.transform.rotozoom(EARTH_IMG, self.__earth_img_angle,
            self.__earth_scale)
        image_position = (self.__center_x - earth_img_rotated.get_width() // 2), \
            self.__surface.get_height() - earth_img_rotated.get_height() // 2

        self.__surface.blit(earth_img_rotated, image_position)


    def __set_dotted_circle_size_and_position(self):
        # size
        size = int(EARTH_IMG.get_width() * self.__earth_scale) + self.__dotted_circle_offset
        self.__dotted_circle = pygame.transform.scale(DOTTED_CIRCLE, (size, size))


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
