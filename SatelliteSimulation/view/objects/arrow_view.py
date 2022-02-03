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
from SatelliteSimulation.view.resources import Color


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class ArrowView:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, start_of_line: tuple, end_of_line: tuple, arrow_head: list, line_thickness: int):
        self.__start_of_line: tuple = start_of_line
        self.__end_of_line: tuple = end_of_line
        self.__arrow_head: list = arrow_head
        self.__line_thickness: int = line_thickness


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    @property
    def start_of_line(self) -> tuple:
        return self.__start_of_line


    @property
    def end_of_line(self) -> tuple:
        return self.__end_of_line


    @property
    def arrow_head(self) -> list:
        return self.__arrow_head


    @property
    def line_thickness(self) -> int:
        return self.__line_thickness


    @property
    def color(self) -> Color:
        return Color.RED

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

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
