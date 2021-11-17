#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
a Border with black background and light grey outline
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pygame
from SatelliteSimulation.view import Color

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class BorderView:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, y: float, width: float, height: float, padding: float):
        self.__border: pygame.Rect = pygame.Rect(x, y, width, height)
        self.__padded_border: pygame.Rect = pygame.Rect(self.__border.x + padding,
            self.__border.y + padding,
            self.__border.width - padding * 2,
            self.__border.height - padding * 2)
        self.__show_padding = False


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_border_rectangle(self):
        return self.__border

    def show_padding(self, show_padding: bool):
        self.__show_padding = show_padding

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def draw(self, surface: pygame.Surface, line_width: int):
        pygame.draw.rect(surface, Color.BLACK, self.__border)
        pygame.draw.rect(surface, Color.LIGHT_GREY, self.__border, line_width)
        if self.__show_padding:
            pygame.draw.rect(surface, Color.RED, self.__padded_border, 1)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #

    def update_size(self, x: float, y: float, width: float, height: float, padding: float):
        self.__border.width = int(width)
        self.__border.height = int(height)
        self.__border.x = int(x)
        self.__border.y = int(y)
        self.__padded_border.x = self.__border.x + padding
        self.__padded_border.y = self.__border.y + padding
        self.__padded_border.width = self.__border.width - padding * 2
        self.__padded_border.height = self.__border.height - padding * 2


#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    pass
