"""
Basic math definitions and calculations.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import numpy as np

from SatelliteSimulation.model.basic_math.vector import *


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


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def __str__(self):
        return f"New equation: g{self.counter}: x(t)={self.direction_vector}t+{self.support_vector}"



    def get_point_in_distance(self, distance: float) -> Vector:
        return add(self.calculate_radial_vector(distance),
                   Vector(self.support_vector[0], self.support_vector[1]))


    def calculate_radial_vector(self, distance: float) -> Vector:
        return multiply(self.unit_normal_direction_vector(), distance)


    def unit_normal_direction_vector(self) -> Vector:
        unit_normal = self.direction_vector / self.direction_vector_magnitude()
        return Vector(unit_normal[0], unit_normal[1])


    def direction_vector_magnitude(self) -> float:
        return np.linalg.norm(self.direction_vector)


    def calculate_t(self, point: tuple) -> float:
        if self.direction_vector[0] != 0:
            t = (point[0] - self.support_vector[0]) / self.direction_vector[0]
            return t
        if self.direction_vector[1] != 0:
            t = (point[1] - self.support_vector[1]) / self.direction_vector[1]
            return t
        return None

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

def vector_to_degree(direction_vector: Vector) -> float:
    angle = math.atan2(direction_vector.y(), direction_vector.x())
    return make_degree_positive(math.degrees(angle))


def make_degree_positive(degrees: float) -> float:
    return (degrees + 360) % 360

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #
