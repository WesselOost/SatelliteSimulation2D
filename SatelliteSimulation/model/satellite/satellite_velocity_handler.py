# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from model.basic_math.vector import *
from model.basic_math.velocity import Velocity


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class SatelliteVelocityHandler:
    """
    Handles the 3 different velocity types disturbance velocity, collision velocity and navigation velocity.
    The three different velocities combined form the actual velocity.
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, max_navigation_velocity_magnitude: float):
        self.__navigation_velocity: Velocity = Velocity(0, 0)
        self.__max_navigation_velocity_magnitude: float = max_navigation_velocity_magnitude
        self.__disturbance_velocity: Velocity = Velocity(0, 0)
        self.__collision_velocity: Velocity = Velocity(0, 0)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def navigation_velocity(self) -> Velocity:
        return self.__navigation_velocity


    def max_navigation_velocity(self) -> float:
        return self.__max_navigation_velocity_magnitude


    def set_navigation_velocity(self, velocity: Vector):
        self.__navigation_velocity.set_vector(velocity)


    def disturbance_velocity(self) -> Velocity:
        return self.__disturbance_velocity


    def collision_velocity(self) -> Velocity:
        return self.__collision_velocity


    def velocity(self) -> Vector:
        return add(self.__navigation_velocity, add(self.__disturbance_velocity, self.__collision_velocity))

    def clear(self):
        self.__navigation_velocity.clear()
        self.__disturbance_velocity.clear()
        self.__collision_velocity.clear()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def update_velocities(self, disturbances: list):
        self.__disturbance_velocity.clear()
        for disturbance in disturbances:
            disturbance.velocity().update()
            self.__disturbance_velocity.add_vector(disturbance.velocity())

        self.__navigation_velocity.update()
        self.__collision_velocity.update()


# ----------------------------------------------------------------------- #
#  SUBSECTION: Private Methods
# ----------------------------------------------------------------------- #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #


