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


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Earth:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, center_x: float, surface_height: float, earth_size: float, dotted_circle_padding):
        self.EARTH_IMG = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "earth.png"))
        self.DOTTED_CIRCLE = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "dashed_circle.png"))
        self.EARTH_IMG.convert()
        self.DOTTED_CIRCLE.convert()

        self.EARTH_IMG = pygame.transform.scale(self.EARTH_IMG, (earth_size, earth_size))
        self.__center_x = center_x
        self.__dotted_circle_padding = dotted_circle_padding
        self.__earth_img_angle = 0

        self.__earth_size = earth_size
        self.__surface_height = surface_height

        self.__dotted_circle_padding = dotted_circle_padding
        dotted_circle_size: float = earth_size + dotted_circle_padding
        dotted_circle_x: float = center_x - (dotted_circle_size // 2)
        dotted_circle_y: float = surface_height - (dotted_circle_size // 2)
        self.__dotted_circle_position: tuple = (dotted_circle_x, dotted_circle_y)
        self.__dotted_circle: pygame.Surface = pygame.transform.scale(self.DOTTED_CIRCLE,
                                                                      (dotted_circle_size, dotted_circle_size))


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def center_x(self) -> float:
        return self.__center_x
    @property
    def surface_height(self) -> float:
        return self.__surface_height
    @property
    def earth_size(self) -> float:
        return self.__earth_size
    @property
    def dotted_circle_padding(self) -> float:
        return self.__dotted_circle_padding

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def draw(self, surface: pygame.Surface):
        surface.blit(self.__dotted_circle, self.__dotted_circle_position)
        self.__rotate_and_draw_earth(surface)


    def get_dotted_circle_position(self) -> tuple:
        return self.__dotted_circle_position[0], self.__dotted_circle_position[1]


    def get_dotted_circle_width(self) -> int:
        return self.__dotted_circle.get_width()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


    def __rotate_and_draw_earth(self, surface: pygame.Surface):
        self.__earth_img_angle -= 0.2
        earth_img_rotated = pygame.transform.rotozoom(self.EARTH_IMG, self.__earth_img_angle, 1)
        image_position = (self.__center_x - earth_img_rotated.get_width() // 2), \
                         surface.get_height() - earth_img_rotated.get_height() // 2

        surface.blit(earth_img_rotated, image_position)


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
