# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Border view for the satellites
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
from model.math.vector import Vector


class SatelliteBorder:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, y: float, width: float, height: float, padding: float):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__padding = padding


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def x(self) -> float:
        return self.__x


    def y(self) -> float:
        return self.__y


    def width(self) -> float:
        return self.__width


    def height(self) -> float:
        return self.__height


    def padding(self) -> float:
        return self.__padding


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def update_scale(self, scale_factor: float):
        self.__x *= scale_factor
        self.__y *= scale_factor
        self.__width *= scale_factor
        self.__height *= scale_factor
        self.__padding *= scale_factor


    def right(self) -> float:
        return self.__x + self.__width - self.__padding


    def left(self) -> float:
        return self.__x + self.__padding


    def top(self) -> float:
        return self.__y + self.__padding


    def bottom(self) -> float:
        return self.__y + self.__height - self.__padding


    def is_object_inside_border(self, center: Vector, radius: float) -> bool:
        return \
            center.x() + radius <= self.right() and \
            center.x() - radius >= self.left() and \
            center.y() + radius <= self.bottom() and \
            center.y() - radius >= self.top()


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
