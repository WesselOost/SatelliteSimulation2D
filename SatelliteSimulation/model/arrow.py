# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
An arrow shape
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import math
from SatelliteSimulation.model.basic_math.vector import *

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
EMPTY_VECTOR = Vector(0, 0)
VELOCITY_ARROW_DEFAULT_SIZE = 24


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class Arrow:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, start_vector: Vector, unit_normal_direction_vector: Vector, magnitude: float):
        '''
        5 vectors that form together an arrow
        the en_of_line is not the end of the arrow, otherwise it would stick out pas the triangular tip of the arrow.

        start_of_line: start coordinates of the line body
        end_of_line: end coordinates of the line body
        head_tip:  coordinates of the tip of the arrow head
        head_left: coordinates of the left corner of the arrow head
        head_right: coordinates of the right corner of the arrow head
        '''
        self.__line_thickness: float = 6
        length: float = magnitude * VELOCITY_ARROW_DEFAULT_SIZE
        if (length > 0):
            self.__start_of_line: Vector = start_vector
            self.__head_tip: Vector = self.__shift_vector_by_length(self.__start_of_line,
                                                                    unit_normal_direction_vector, length)

            self.__end_of_line: Vector = self.__shift_vector_by_length(self.__head_tip, self.__start_of_line,
                                                                       self.__line_thickness)

            start_of_arrow_head = self.__shift_vector_by_length(self.__head_tip, self.__start_of_line,
                                                                self.__line_thickness * 3)
            self.__head_left: Vector = self.__rotate_point_around_axis(start_of_arrow_head, self.__head_tip,
                                                                       math.pi / 6)
            self.__head_right: Vector = self.__rotate_point_around_axis(start_of_arrow_head, self.__head_tip,
                                                                        -math.pi / 6)
        else:
            self.__start_of_line: Vector = EMPTY_VECTOR.__copy__()
            self.__end_of_line: Vector = EMPTY_VECTOR.__copy__()
            self.__head_tip: Vector = EMPTY_VECTOR.__copy__()
            self.__head_left: Vector = EMPTY_VECTOR.__copy__()
            self.__head_right: Vector = EMPTY_VECTOR.__copy__()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def start_of_line(self) -> tuple:
        return self.__start_of_line.get_as_tuple()


    def end_of_line(self) -> tuple:
        return self.__end_of_line.get_as_tuple()


    def head_tip(self) -> tuple:
        return self.__head_tip.get_as_tuple()


    def head_left(self) -> tuple:
        return self.__head_left.get_as_tuple()


    def head_right(self) -> tuple:
        return self.__head_right.get_as_tuple()


    def line_thickness(self) -> int:
        return max(1, int(self.__line_thickness))


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


    def __shift_vector_by_length(self, start_position: Vector, direction_vector: Vector, length: float) -> Vector:
        distance: float = calculate_distance(direction_vector, start_position)
        dx_dy: Vector = subtract(direction_vector, start_position)
        unit_normal_direction_vector: Vector = divide(dx_dy, distance)
        scaled_direction_vector: Vector = multiply(unit_normal_direction_vector, length)
        return add(start_position, scaled_direction_vector)


    def __rotate_point_around_axis(self, point: Vector, axis: Vector, theta: float) -> Vector:
        sin: float = math.sin(theta)
        cos: float = math.cos(theta)
        d: Vector = subtract(point, axis)  # (dx, dy)
        x: float = cos * d.x() - sin * d.y() + axis.x()
        y: float = sin * d.x() + cos * d.y() + axis.y()
        return Vector(x, y)


    def __clear(self):
        pass

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


if __name__ == '__main__':
    pass
