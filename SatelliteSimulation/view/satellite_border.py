#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Link    : link
# @Version : 0.0.1
"""
a Border with black background and light grey outline
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pygame

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
LIGHT_GREY = (243, 243, 243)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class Border:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, y: float, width: float, height: float, margin: float, padding: float):
        self.__float_x: float = x + margin
        self.__float_y: float = y + margin
        self.__float_width: float = (width - margin * 2)
        self.__float_height: float = (height - margin)
        self.__margin: float = margin
        self.__padding: float = padding

        self.__border: pygame.Rect = pygame.Rect(self.__float_x, self.__float_y, self.__float_width,
                                                 self.__float_height)
        self.__show_offset = False


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_border(self):
        return self.__border


    def get_padding(self) -> int:
        return int(self.__padding)


    def show_offset(self):
        self.__show_offset = True


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def draw(self, surface: pygame.Surface, line_width: int):
        pygame.draw.rect(surface, BLACK, self.__border)
        pygame.draw.rect(surface, LIGHT_GREY, self.__border, line_width)
        if self.__show_offset:
            border = self.__border.copy()
            border.x += self.get_padding()
            border.y += self.get_padding()
            border.width -= self.get_padding() * 2
            border.height -= self.get_padding() * 2
            pygame.draw.rect(surface, RED, border, 1)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    def on_size_changed(self, scale_factor: float):
        self.__float_width *= scale_factor
        self.__border.width = int(self.__float_width)
        self.__float_height *= scale_factor
        self.__border.height = int(self.__float_height)
        self.__float_x *= scale_factor
        self.__border.x = int(self.__float_x)
        self.__float_y *= scale_factor
        self.__border.y = int(self.__float_y)
        self.__margin *= scale_factor
        self.__padding *= scale_factor


#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    pass
