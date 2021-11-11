#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Basic math definitions and calculations.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import numpy as np
from numpy.core.numeric import False_

from SatelliteSimulation.model.math.vector import *


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class StraightLineEquation:
    counter = 1


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, vector1: tuple, vector2: tuple):
        self.stack = np.vstack([vector1, vector2])
        self.direction_vector: np.array = np.array(vector2) - np.array(vector1)
        self.support_vector: np.array = np.array(vector1)
        self.counter = StraightLineEquation.counter
        StraightLineEquation.counter += 1
        self.print_equation()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def print_equation(self):
        pass
        # print(f"New equation: g{self.counter}: x(t)={self.direction_vector}t+{self.support_vector}")


    def calculate_new_point(self, t: float) -> tuple:
        return tuple(map(self.direction_vector * t * self.support_vector))


    def calculate_t_for_distance(self, distance: float) -> tuple:
        t = distance / np.linalg.norm(self.direction_vector)
        return t, -t


    def calculate_t(self, point: tuple) -> float:
        # TODO fix RuntimeWarning: divide by zero encountered in double_scalars
        return (point[0] - self.support_vector[0]) / self.direction_vector[0]
    
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


class LinearSystemOfEquations:
    def get_intersection(self, g1: StraightLineEquation, g2: StraightLineEquation) -> tuple:
        """
        The two 2D straight line equations are checked if there is a intersection point
        
        Parameters
        ----------
        straightLineEquation1 : StraightLineEquation
            g1: x(t)=a*t1+b
        straightLineEquation2 : StraightLineEquation
            g2: x(t)=a*t2+b

        Returns
        -------
        tuple
            intersection point, (inf,inf) if no or infinity intersections 
        """
        stack = np.vstack([g1.stack, g2.stack])
        homogeneous = np.hstack((stack, np.ones((4, 1))))
        line1 = np.cross(homogeneous[0], homogeneous[1])
        line2 = np.cross(homogeneous[2], homogeneous[3])
        x, y, z = np.cross(line1, line2)
        if z == 0:
            return (float('inf'), float('inf'))
        return (x / z, y / z)

    def check_collinearity(self, g1: StraightLineEquation, g2: StraightLineEquation) -> bool:
        t_x = (g1.support_vector[0] - g2.support_vector[0])/g2.direction_vector[0]
        t_y = (g1.support_vector[1] - g2.support_vector[1])/g2.direction_vector[1]
        factor_x = g2.direction_vector[0]/g1.direction_vector[0]
        factor_y = g2.direction_vector[1]/g1.direction_vector[1]
        if t_x == t_y and factor_x==factor_y and factor_x <= 0:
            return True
        return False
        
        # =========================================================================== #
        #  SECTION: Function definitions
        # =========================================================================== #

        # =========================================================================== #
        #  SECTION: Main Body
        # =========================================================================== #

if __name__ == '__main__':
    pass
