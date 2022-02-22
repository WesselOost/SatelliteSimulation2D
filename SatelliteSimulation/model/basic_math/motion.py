# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import numpy as np

from model.basic_math.math_basic import StraightLineEquation
from model.basic_math.vector import Vector
from model.collision.future_collision_data import FutureCollisionData


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
        self.direction_vector: np.array = None
        self.type: int = 1
        self.support_vector: np.array = self.points[-1]
        self.velocity: np.array = None
        self.acceleration: np.array = None
        self.jerk = None
        self.motion_duration: float = 1E5  # value faaaar in the future
        self._set_basic_features()
        self._set_motion_duration()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_direction_vector(self) -> Vector:
        return Vector(self.direction_vector[0], self.direction_vector[1])


    def get_current_position(self) -> Vector:
        current_position = self.points[-1]
        return Vector(current_position[0], current_position[1])


    def calculate_point_one_trajectory(self, t: float) -> np.array:
        return self.jerk / 3 * t ** 3 + self.acceleration / 2 * t ** 2 + self.velocity * t + self.support_vector


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def _set_basic_features(self):
        if len(self.points) == 1:
            self.type = 1
            self.velocity = np.zeros(2)
            self.acceleration = np.zeros(2)
            self.jerk = np.zeros(2)
        if len(self.points) == 2:
            self.type = 2
            self.velocity = self.points[1] - self.points[0]
            self.acceleration = np.zeros(2)
            self.jerk = np.zeros(2)
        elif len(self.points) == 3:
            self.type = 3
            self.velocity = self.points[1] - self.points[0]
            velocity2: np.array = self.points[2] - self.points[1]
            self.acceleration = velocity2 - self.velocity
            self.jerk = np.zeros(2)
        elif len(self.points) >= 4:
            self.type = 4
            self.velocity = self.points[1] - self.points[0]
            velocity2: np.array = self.points[2] - self.points[1]
            velocity3: np.array = self.points[3] - self.points[2]
            self.acceleration = velocity2 - self.velocity
            acceleration2: np.array = velocity3 - velocity2
            self.jerk = acceleration2 - self.acceleration
        else:
            pass
        self.direction_vector = self.velocity


    def _set_motion_duration(self):
        j_x, j_y = self.jerk
        a_x, a_y = self.acceleration
        v_x0, v_y0 = self.velocity

        coeff_1 = (j_x ** 2 + j_y ** 2) / 4
        coeff_2 = j_x * a_x + j_y * a_y
        coeff_3 = j_x * v_x0 + j_y * v_y0
        coeff_4 = a_x ** 2 + a_y ** 2
        coeff_5 = 2 * (a_x * v_x0 + a_y * v_y0)
        coeff_6 = v_x0 ** 2 + v_y0 ** 2

        velocity_equation = np.array([coeff_1, coeff_2,
                                      coeff_3 + coeff_4,
                                      coeff_5, coeff_6])
        roots = np.roots(velocity_equation)
        rational_roots_from_zero = [z.real for z in roots if z.imag == 0 and z.real >= 0]
        if len(rational_roots_from_zero) == 2 and rational_roots_from_zero[0].real == 0:
            self.motion_duration = rational_roots_from_zero[1]


class FutureCollisionDetector:
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self,
                 radius1: float,
                 radius2: float,
                 trajectory1: Trajectory,
                 trajectory2: Trajectory):
        self.radius1 = radius1
        self.radius2 = radius2
        self._trajectory1 = trajectory1
        self._trajectory2 = trajectory2
        self._min_distance = self.radius1 + self.radius2
        self._end_of_motions = self._trajectory1.motion_duration + \
                               self._trajectory2.motion_duration


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def is_collision_possible(self) -> FutureCollisionData:
        return self._solve_distance_equation_for_four()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def _print_roots(roots: list):
        print(f"Roots: ")
        for i, z in enumerate(roots):
            if z.imag == 0:
                print(f"\tx_{i + 1} = {z.real:.2}")
            else:
                print(f"\tx_{i + 1} = {z.real:.2} {z.imag:+.2}")


    def _get_point_of_crash(self, point1: tuple, point2: tuple) -> tuple:
        radial_vector: Vector = StraightLineEquation(
            point2, point1).get_point_in_distance(self.radius1)
        return radial_vector.get_as_tuple()


    def _solve_distance_equation_for_two(self) -> FutureCollisionData:
        v_x1, v_y1 = self._trajectory1.velocity
        v_x2, v_y2 = self._trajectory2.velocity
        p_x1, p_y1 = self._trajectory1.support_vector
        p_x2, p_y2 = self._trajectory2.support_vector

        v_x = v_x2 - v_x1
        v_y = v_y2 - v_y1
        p_x = p_x2 - p_x1
        p_y = p_y2 - p_y1

        coeff_1 = v_x ** 2 + v_y ** 2
        coeff_2 = v_x * p_x + v_y * p_y
        coeff_3 = p_x ** 2 + p_y ** 2 - self._min_distance ** 2

        distance_equation = np.array([coeff_1, coeff_2, coeff_3])
        roots = np.roots(distance_equation)
        critical_moments = [z.real for z in roots if z.imag == 0 and 0 <= z.real <= self._end_of_motions]
        if critical_moments:
            t = min(critical_moments)
            x1_crash = v_x1 * t + p_x1
            x2_crash = v_x2 * t + p_x2
            y1_crash = v_y1 * t + p_y1
            y2_crash = v_y2 * t + p_y2
            point_of_crash = self._get_point_of_crash(
                (x1_crash, y1_crash), (x2_crash, y2_crash))
            return FutureCollisionData(point_of_crash, t, self._trajectory2)
        return None


    def _solve_distance_equation_for_three(self) -> FutureCollisionData:
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

        coeff_1 = a_x ** 2 + a_y ** 2
        coeff_2 = 2 * (a_x * v_x + a_y * v_y)
        coeff_3 = 2 * (a_x * p_x + a_y * p_y)
        coeff_4 = v_x ** 2 + v_y ** 2
        coeff_5 = 2 * (v_x * p_x + v_y * p_y)
        coeff_6 = p_x ** 2 + p_y ** 2 - self._min_distance ** 2

        distance_equation = np.array([coeff_1, coeff_2, coeff_3 + coeff_4, coeff_5, coeff_6])
        roots = np.roots(distance_equation)
        critical_moments = [
            z.real for z in roots if z.imag == 0 and 0 <= z.real <= self._end_of_motions]
        if critical_moments:
            t = min(critical_moments)
            x1_crash = a_x1 / 2 * t ** 2 + v_x1 * t + p_x1
            x2_crash = a_x2 / 2 * t ** 2 + v_x2 * t + p_x2
            y1_crash = a_y1 / 2 * t ** 2 + v_y1 * t + p_y1
            y2_crash = a_y2 / 2 * t ** 2 + v_y2 * t + p_y2
            point_of_crash = self._get_point_of_crash(
                (x1_crash, y1_crash), (x2_crash, y2_crash))
            return FutureCollisionData(point_of_crash, t, self._trajectory2)
        return None


    def _solve_distance_equation_for_four(self) -> FutureCollisionData:
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

        coeff_1 = j_x ** 2 + j_y ** 2
        coeff_2 = 2 * (a_x * j_x + a_y * j_y)
        coeff_3 = 2 * (j_x * v_x + j_y * v_y)
        coeff_4 = a_x ** 2 + a_y ** 2
        coeff_5 = 2 * (j_x * p_x + j_y * p_y)
        coeff_6 = 2 * (v_x * a_x + v_y * a_y)
        coeff_7 = 2 * (a_x * p_x + a_y * p_y)
        coeff_8 = v_x ** 2 + v_y ** 2
        coeff_9 = 2 * (v_x * p_x + v_y * p_y)
        coeff_10 = p_x ** 2 + p_y ** 2 - self._min_distance ** 2

        distance_equation = np.array(
            [coeff_1, coeff_2,
             coeff_3 + coeff_4,
             coeff_5 + coeff_6,
             coeff_7 + coeff_8,
             coeff_9, coeff_10])
        roots = np.roots(distance_equation)
        critical_moments = [z.real for z in roots if z.imag ==
                            0 and 0 < z.real <= self._end_of_motions]
        if critical_moments:
            t = min(critical_moments)
            x1_crash = j_x1 / 3 * t ** 3 + a_x1 / 2 * t ** 2 + v_x1 * t + p_x1
            x2_crash = j_x2 / 3 * t ** 3 + a_x2 / 2 * t ** 2 + v_x2 * t + p_x2
            y1_crash = j_y1 / 3 * t ** 3 + a_y1 / 2 * t ** 2 + v_y1 * t + p_y1
            y2_crash = j_y2 / 3 * t ** 3 + a_y2 / 2 * t ** 2 + v_y2 * t + p_y2
            point_of_crash = self._get_point_of_crash(
                (x1_crash, y1_crash), (x2_crash, y2_crash))
            return FutureCollisionData(point_of_crash, t, self._trajectory2)
        return None


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def direction_changed(points: list) -> bool:
    """
    checks if first, last and second last points are in one line

    Returns
    -------
    bool
        True, if the direction has changed.
        the second last point is not a possible solution from
        the straigt line equation of the first and the last point
    """
    if len(points) <= 2:
        return False
    straight_line_eq = StraightLineEquation(points[0], points[-1])
    moment_of_where_point_was = straight_line_eq.calculate_t(points[-2])
    
    return moment_of_where_point_was is None or moment_of_where_point_was > 1


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    """tray1: Trajectory = Trajectory([(1756.5, 74.5)]*4)
    tray2: Trajectory= Trajectory([(0,0)]*4)
    tray2.support_vector = np.array((1644.3000000000002, 195.46))
    tray2.velocity = np.array((0, -3.9099999999999966))
    tray2.jerk = np.array((0, 0.020000000000010232))
    tray2.acceleration = np.array((0, -0.05000000000001137))
    collision = FutureCollisionDetecter(32.5, 32.5, tray2, tray1).is_collision_possible()
    if collision:
        new_pos_of_1 = tray1.calculate_point_one_trajectory(collision.time())
        new_pos_of_2 = tray2.calculate_point_one_trajectory(collision.time())
        print(collision.position(), collision.time())
        print(calculate_distance(collision.position(), Vector(new_pos_of_2[0], new_pos_of_2[1])))
        print(calculate_distance(collision.position(),
              Vector(new_pos_of_1[0], new_pos_of_1[1])))
    else:
        print(None)"""
    pass