# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Class description
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
from SatelliteSimulation.model.math.vector import Vector, divide, multiply


class Velocity(Vector):

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, y: float, acceleration=0.0):
        vector = Vector(x, y)
        if vector.magnitude() > 0:
            # normalized vector
            vector = divide(vector, vector.magnitude())
        super().__init__(vector.x(), vector.y())

        self.__acceleration: float = acceleration


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def acceleration(self) -> float:
        return self.__acceleration


    def set_acceleration(self, acceleration: float):
        self.__acceleration = acceleration


    def update_scale(self, scale_factor: float):
        self.__acceleration *= scale_factor
        self.set_vector(multiply(Vector(self.x(), self.y()), scale_factor))


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
