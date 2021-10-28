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
import math
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
        self.direction_vector: np.array = np.array(vector2)-np.array(vector1)
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
        print(f"New equation: g{self.counter}: x(t)={self.direction_vector}t+{self.support_vector}")

    def calculate_new_point(self, t: float) -> np.array:
        return self.direction_vector * t * self.support_vector
    
    def calculate_t_for_distance(self, distance: float) -> tuple:
        t = distance/np.linalg.norm(self.direction_vector)
        return t, -t
    
    def calculate_t(self, point:tuple)->float:
        return (point[0] - self.support_vector[0])/self.direction_vector[0]
      
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
        homogenous = np.hstack((stack, np.ones((4,1))))
        line1 = np.cross(homogenous[0], homogenous[1])
        line2 = np.cross(homogenous[2], homogenous[3])
        x, y, z = np.cross(line1, line2)
        if z == 0:
            return (float('inf'), float('inf'))
        return (x/z, y/z)


        # =========================================================================== #
        #  SECTION: Function definitions
        # =========================================================================== #

        # =========================================================================== #
        #  SECTION: Main Body
        # =========================================================================== #


if __name__ == '__main__':
    pass
