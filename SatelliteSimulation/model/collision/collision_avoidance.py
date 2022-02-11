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
from hashlib import new
from SatelliteSimulation.model.basic_math.math_basic import vector_to_degree
from SatelliteSimulation.model.basic_math.vector import Vector, add, calculate_distance, multiply


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class CollisionAvoidanceHandler:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, satellite_center: Vector,
                 observed_satellite_center: Vector,
                 observed_satellite_direction: Vector):
        self.__satellite_center = satellite_center
        self.__observed_satellite_center = observed_satellite_center
        self.__observed_satellite_direction = observed_satellite_direction


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def calculate_degrees_avoiding_satellite_direction_by_90_degrees(self) -> float:
        avoidance_vector: Vector = self.__observed_satellite_direction.tangent()
        initial_distance: float = calculate_distance(self.__satellite_center, self.__observed_satellite_center)
        test_distance: float = calculate_distance(
            add(self.__satellite_center, avoidance_vector.unit_normal()),
            self.__observed_satellite_center)
        if test_distance >= initial_distance:
            return vector_to_degree(avoidance_vector)
        return vector_to_degree(multiply(avoidance_vector, -1))

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