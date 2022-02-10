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
from SatelliteSimulation.model.basic_math.math_basic import make_degrees_positive, vector_to_degrees, inverse_degrees
from SatelliteSimulation.model.basic_math.vector import Vector, subtract


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
        observed_satellite_towards_satellite: Vector = subtract(self.__satellite_center,
                                                                self.__observed_satellite_center)

        observed_satellite_direction_degrees: float = make_degrees_positive(
            vector_to_degrees(self.__observed_satellite_direction))
        inverted_observed_satellite_direction_degrees: float = inverse_degrees(observed_satellite_direction_degrees)
        observed_s_towards_satellite_s_degrees: float = make_degrees_positive(
            vector_to_degrees(observed_satellite_towards_satellite))
        min_degrees = min(observed_satellite_direction_degrees, inverted_observed_satellite_direction_degrees)
        max_degrees = max(observed_satellite_direction_degrees, inverted_observed_satellite_direction_degrees)

        if min_degrees < observed_s_towards_satellite_s_degrees <= max_degrees:
            result: float = min_degrees + 90
        else:
            result: float = min_degrees - 90

        result = make_degrees_positive(result)
        return result


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
