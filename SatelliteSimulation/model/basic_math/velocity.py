# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from model.basic_math.vector import Vector, multiply
import numpy as np


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class Velocity(Vector):
    """
    Velocity which can accelerate and decelerate.
    """


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.__t = 0
        self.__v1 = 0
        self.__v2 = 0
        self.__magnitude = 0


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def update(self):
        if self.__v1 != 0 or self.__v2 != 0:
            self.increment_t()
            self.update_magnitude()
            if self.__t > 0 and self.__magnitude <= 0:
                self.__t = 0
                self.__v1 = 0
                self.__v2 = 0
                self.__magnitude = 0
                self.set_xy(0, 0)
            else:
                self.set_vector(multiply(self.unit_normal(), self.__magnitude))


    def dummy_update(self, moments_in_future: int) -> Vector:
        if self.__v1 != 0 or self.__v2 != 0:
            t = self.__t + moments_in_future
            future_magnitude = self.__v1 * t ** 2 + self.__v2 * t
            if t > 0 and future_magnitude <= 0:
                return Vector(0, 0)
            return multiply(self.unit_normal(), future_magnitude)


    def t(self):
        return self.__t


    def set_t(self, new_t: float):
        self.__t: float = new_t


    def increment_t(self):
        self.__t += 1


    def update_scale(self, scale_factor: float):
        self.set_vector(multiply(Vector(self.x(), self.y()), scale_factor))


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def solve_equation_and_set_v1_v2(self, v_max: float, t_vertex: float):
        matrix_A = np.array([[t_vertex ** 2, t_vertex], [(2 * t_vertex) ** 2, 2 * t_vertex]])
        matrix_B = np.array([v_max, 0])
        result = np.linalg.inv(matrix_A).dot(matrix_B)
        self.__v1 = result[0]
        self.__v2 = result[1]


    def update_magnitude(self):
        self.__magnitude = self.__v1 * self.__t ** 2 + self.__v2 * self.__t

# ----------------------------------------------------------------------- #
#  SUBSECTION: Private Methods
# ----------------------------------------------------------------------- #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
