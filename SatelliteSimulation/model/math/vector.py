# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
a 2 dimensional vector class
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import math


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class Vector:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def x(self):
        return self._x


    def y(self):
        return self._y


    def get_as_tuple(self) -> tuple:
        return self._x, self._y


    def set_x(self, x: float):
        self._x = x


    def set_y(self, y: float):
        self._y = y


    def set_vector(self, vector):
        self._x = vector.x()
        self._y = vector.y()


    def set_xy(self, x: float, y: float):
        self._x = x
        self._y = y


    def clear(self):
        self.set_x(0)
        self.set_y(0)


    def magnitude(self) -> float:
        return math.sqrt(self._x ** 2 + self._y ** 2)


    def tangent(self):
        return Vector(-self.y(), self.x())


    def dot_product(self, vector):
        return self._x * vector.x() + self._y * vector.y()
    


    def __copy__(self):
        return Vector(self._x, self._y)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def add_to_x(self, x: float):
        self._x += x


    def add_to_y(self, y: float):
        self._y += y

    def add_vector(self, vector):
        self.add_to_x(vector.x())
        self.add_to_y(vector.y())


    def __str__(self):
        return f"({self._x}, {self._y})"
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #


def add(vector1: Vector, vector2: Vector) -> Vector:
    return Vector(vector1.x() + vector2.x(), vector1.y() + vector2.y())


def subtract(vector1: Vector, vector2: Vector) -> Vector:
    return Vector(vector1.x() - vector2.x(), vector1.y() - vector2.y())


def multiply(vector: Vector, scalar: float):
    return Vector(vector.x() * scalar, vector.y() * scalar)


def divide(vector: Vector, scalar: float):
    if scalar != 0:
        return Vector(vector.x() / scalar, vector.y() / scalar)
    else:
        print("check vector division")


def calculate_distance(vector1: Vector, vector2: Vector) -> float:
    vector: Vector = subtract(vector1, vector2)
    return vector.magnitude()

def tuple_to_vector(given_tuple:tuple)->Vector:
    return Vector(given_tuple[0],given_tuple[1])


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


if __name__ == '__main__':
    pass
