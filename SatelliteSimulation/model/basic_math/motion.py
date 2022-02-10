#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022-02-09 15:36:37
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Short Introduction
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import numpy as np

from SatelliteSimulation.model.collision import Collision


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class Trajectory:
    """
        This class describes the motion of object in the simulation.
        The trajectories are based on the defined motion processes.
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, points: list):
        self.points: list = [np.array(point) for point in points]
        self.direction_vector: np.array = self.points[1] - self.points[0]
        self.type: int = 1
        self.support_vector: np.array = self.points[0]
        self.velocity: np.array = None
        self.acceleration: np.array = None
        self.jerk = None
        self._set_basic_features()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def _set_basic_features(self):
        if len(self.points) == 2:
            self.type = 2
            self.velocity = self.direction_vector
        elif len(self.points) == 3:
            self.type = 3
            self.velocity = self.direction_vector
            self.acceleration = self.points[2] - self.points[1] - self.velocity
        elif len(self.points) >= 4:
            self.type = 4
            self.velocity = self.points[-3] - self.points[-4]
            self.acceleration = self.points[-2] - self.points[-3] - self.velocity
            self.jerk = self.points[-1] - self.points[-2] - self.acceleration
        else:
            pass

class CollisionDetecter:
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self,
                 min_distance: float,
                 trajectory1: Trajectory,
                 trajectory2: Trajectory):
        self._min_distance = min_distance
        self._trajectory1 = trajectory1
        self._trajectory2 = trajectory2

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def is_collision_possible(self) -> float:
        type1 = self._trajectory1.type
        type2 = self._trajectory2.type
        if type1 != type2:
            print(f"type error: {type1}!={type2}")
            return
        if type1 == 2:
            return self._solve_distance_equation_for_two()
        elif type1 == 3:
            return self._solve_distance_equation_for_three()
        elif type1 == 4:
            return self._solve_distance_equation_for_four()
        else:
            return None
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def _print_roots(roots:list):
        print(f"Roots: ")
        for i, z in enumerate(roots):
            if z.imag == 0:
                print(f"\tx_{i+1} = {z.real:.2}")
            else:
                print(f"\tx_{i+1} = {z.real:.2} {z.imag:+.2}")

    def _solve_distance_equation_for_two(self) -> Collision:
        v_x1, v_y1 = self._trajectory1.velocity
        v_x2, v_y2 = self._trajectory2.velocity
        p_x1, p_y1 = self._trajectory1.support_vector
        p_x2, p_y2 = self._trajectory2.support_vector

        v_x = v_x2 - v_x1
        v_y = v_y2 - v_y1
        p_x = p_x2 - p_x1
        p_y = p_y2 - p_y1

        coeff_1 = v_x**2 + v_y**2
        coeff_2 = v_x * p_x + v_y * p_y
        coeff_3 = p_x**2 + p_y**2 - self._min_distance**2

        distance_equation = np.array([coeff_1, coeff_2, coeff_3])
        roots = np.roots(distance_equation)
        critical_moments = [z.real for z in roots if z.imag == 0 and z.real > 0]
        if critical_moments:
            t = min(critical_moments)
            x1_crash = v_x1 * t + p_x1
            x2_crash = v_x2 * t + p_x2
            y1_crash = v_y1 * t + p_y1
            y2_crash = v_y2 * t + p_y2
            point_of_crash = (x1_crash + x2_crash) / \
                2, (y1_crash + y2_crash) / 2
            return Collision(point_of_crash, t)
        return None

    def _solve_distance_equation_for_three(self) -> Collision:
        a_x1, a_y1 = self._trajectory1.acceleration
        a_x2, a_y2 = self._trajectory2.acceleration
        v_x1, v_y1 = self._trajectory1.velocity
        v_x2, v_y2 = self._trajectory2.velocity
        p_x1, p_y1 = self._trajectory1.support_vector
        p_x2, p_y2 = self._trajectory2.support_vector

        a_x = (a_x2 - a_x1) / 2
        a_y = (a_y2 - a_y1) / 2
        v_x = v_x2 - v_x1
        v_y = v_y2 - v_y1
        p_x = p_x2 - p_x1
        p_y = p_y2 - p_y1

        coeff_1 = a_x**2 + a_y**2
        coeff_2 = 2 * (a_x * v_x + a_y + v_y)
        coeff_3 = 2 * (a_x * p_x + a_y + p_y)
        coeff_4 = v_x**2 + v_y**2
        coeff_5 = 2 * (v_x * p_x + v_y * p_y)
        coeff_6 = p_x**2 + p_y**2 - self._min_distance**2

        distance_equation = np.array([coeff_1, coeff_2, coeff_3, coeff_4, coeff_5, coeff_6])
        roots = np.roots(distance_equation)
        critical_moments = [
            z.real for z in roots if z.imag == 0 and z.real >= 0]
        if critical_moments:
            t = min(critical_moments)
            x1_crash = a_x1 / 2 * t**2 + v_x1 * t + p_x1
            x2_crash = a_x2 / 2 * t**2 + v_x2 * t + p_x2
            y1_crash = a_y1 / 2 * t**2 + v_y1 * t + p_y1
            y2_crash = a_y2 / 2 * t**2 + v_y2 * t + p_y2
            point_of_crash = (x1_crash + x2_crash) / \
                2, (y1_crash + y2_crash) / 2
            return Collision(point_of_crash, t)
        return None

    def _solve_distance_equation_for_four(self) -> Collision:
        j_x1, j_y1 = self._trajectory1.jerk
        j_x2, j_y2 = self._trajectory2.jerk
        a_x1, a_y1 = self._trajectory1.acceleration
        a_x2, a_y2 = self._trajectory2.acceleration
        v_x1, v_y1 = self._trajectory1.velocity
        v_x2, v_y2 = self._trajectory2.velocity
        p_x1, p_y1 = self._trajectory1.support_vector
        p_x2, p_y2 = self._trajectory2.support_vector

        j_x = (j_x2 - j_x1) / 3
        j_y = (j_y2 - j_y1) / 3
        a_x = (a_x2 - a_x1) / 2
        a_y = (a_y2 - a_y1) / 2
        v_x = v_x2 - v_x1
        v_y = v_y2 - v_y1
        p_x = p_x2 - p_x1
        p_y = p_y2 - p_y1

        coeff_1 = j_x**2 + j_y**2
        coeff_2 = 2 * (a_x * j_x + a_y + j_y)
        coeff_3 = 2 * (j_x * v_x + j_y + v_y)
        coeff_4 = a_x**2 + a_y**2
        coeff_5 = 2 * (j_x * p_x + j_y * p_y)
        coeff_6 = 2 * (v_x * a_x + v_y * a_y)
        coeff_7 = 2 * (a_x * p_x + a_y + p_y)
        coeff_8 = v_x**2 + v_y**2
        coeff_9 = 2 * (v_x * p_x + v_y * p_y)
        coeff_10 = p_x**2 + p_y**2 - self._min_distance**2

        distance_equation = np.array(
            [coeff_1, coeff_2, coeff_3, coeff_4, coeff_5,
             coeff_6, coeff_7, coeff_8, coeff_9, coeff_10])
        roots = np.roots(distance_equation)
        critical_moments = [z.real for z in roots if z.imag == 0 and z.real >= 0]
        if critical_moments:
            t = min(critical_moments)
            x1_crash = j_x1 / 3 * t **3 + a_x1 / 2 * t**2 + v_x1 * t + p_x1
            x2_crash = j_x2 / 3 * t ** 3 + a_x2 / 2 * t**2 + v_x2 * t + p_x2
            y1_crash = j_y1 / 3 * t ** 3 + a_y1 / 2 * t**2 + v_y1 * t + p_y1
            y2_crash = j_y2 / 3 * t ** 3 + a_y2 / 2 * t**2 + v_y2 * t + p_y2
            point_of_crash = (x1_crash + x2_crash) / \
                2, (y1_crash + y2_crash) / 2
            return Collision(point_of_crash, t)
        return None



# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    traj_1 = Trajectory([(0, 0), (0, 0), (0, 0), (0, 0)])
    traj_2 = Trajectory([(0, 1), (0, 0), (0, 0), (0, 0)])
    dist = 1

    print(CollisionDetecter(dist, traj_1, traj_2).is_collision_possible())

