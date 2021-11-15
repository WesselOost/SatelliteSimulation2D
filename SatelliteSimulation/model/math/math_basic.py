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

from model.math.vector import *


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
        return tuple(self.direction_vector * t * self.support_vector)


    def calculate_t_for_distance(self, distance: float) -> tuple:
        t = distance / self.direction_vector_magnitude()
        return t, -t
    
    def direction_vector_magnitude(self) -> float:
        return np.linalg.norm(self.direction_vector)

    def calculate_t(self, point: tuple) -> float:
        if self.direction_vector[0] != 0:
            t = (point[0] - self.support_vector[0])/self.direction_vector[0]
            return t 
        if self.direction_vector[1] != 0:
            t = (point[1] - self.support_vector[1])/self.direction_vector[1]
            return t 
        else:
            return None
    
    def distance_to_point(self, point:tuple)->float:
        location_vector = np.array(point)
        return np.linalg.norm(np.cross(location_vector - self.support_vector, self.direction_vector))/self.direction_vector_magnitude()
    
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

    def check_identity(self, g1: StraightLineEquation, g2: StraightLineEquation) -> bool:
        # 1. test if the direction vectors are collinear, vector1 = factor * vector2?
        parallelism:bool = self.__check_parallelism(g1, g2)
        if parallelism:
            # 2. test if g1 support vector can be calculated by g2 (the same t variable for both dimensions)
            if g2.direction_vector[0] != 0:
                t = (g1.support_vector[0] - g2.support_vector[0])/g2.direction_vector[0]
                return t >= 0 and g2.calculate_new_point(t)[1] == g1.support_vector[1]
            if g2.direction_vector[1] != 0:
                t = (g1.support_vector[1] - g2.support_vector[1])/g2.direction_vector[1]
                return t >= 0 and g2.calculate_new_point(t)[0] == g1.support_vector[0]
        return False
    
    def calculate_point_and_moment_of_crash(self, g1: StraightLineEquation, g2: StraightLineEquation) -> tuple:
        distance = np.linalg(g1.support_vector - g2.support_vector)
        velocity1 = g1.direction_vector_magnitude()
        velocity2 = g2.direction_vector_magnitude()
        t = (velocity1 + velocity2)/distance
        return g1.calculate_new_point(t), t
    
    def __check_parallelism(self, g1: StraightLineEquation, g2: StraightLineEquation)->bool:
        if g2.direction_vector[0] != 0:
            factor = g1.direction_vector[0]/g2.direction_vector[0]
            return g1.direction_vector[1] * factor == g2.direction_vector[1]
        if g2.direction_vector[1] != 0:
            factor = g1.direction_vector[1]/g2.direction_vector[1]
            return g1.direction_vector[0] * factor == g2.direction_vector[0]
        print("DEBUG: __check_parallelism() was not successful -.-")

    
        # =========================================================================== #
        #  SECTION: Function definitions
        # =========================================================================== #

        # =========================================================================== #
        #  SECTION: Main Body
        # =========================================================================== #

if __name__ == '__main__':
    pass
