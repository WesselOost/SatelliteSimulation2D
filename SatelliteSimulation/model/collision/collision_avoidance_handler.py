# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import random

from SatelliteSimulation.model.basic_math.math_basic import vector_to_degree
from SatelliteSimulation.model.basic_math.vector import Vector, add, calculate_distance, multiply


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


# ----------------------------------------------------------------------- #
#  SUBSECTION: Constructor
# ----------------------------------------------------------------------- #


# ----------------------------------------------------------------------- #
#  SUBSECTION: Getter/Setter
# ----------------------------------------------------------------------- #

# ----------------------------------------------------------------------- #
#  SUBSECTION: Public Methods
# ----------------------------------------------------------------------- #

# ----------------------------------------------------------------------- #
#  SUBSECTION: Private Methods
# ----------------------------------------------------------------------- #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def calculate_random_degrees():
    return random.randint(0, 360)

def calculate_degrees_which_avoids_object_by_90_degrees(observed_object_direction: Vector,
                                                        observed_object_center: Vector,
                                                        satellite_direction: Vector,
                                                        satellite_center: Vector):
    if observed_object_direction.magnitude():
        avoidance_direction: Vector = observed_object_direction.tangent()
    else:
        avoidance_direction: Vector = satellite_direction.tangent()

    initial_distance: float = calculate_distance(vector1=satellite_center,
                                                 vector2=observed_object_center)

    temp_new_satellite_position: Vector = add(vector1=satellite_center,
                                              vector2=avoidance_direction.unit_normal())

    test_distance: float = calculate_distance(vector1=temp_new_satellite_position,
                                              vector2=observed_object_center)

    if test_distance >= initial_distance:
        return vector_to_degree(direction_vector=avoidance_direction)
    return vector_to_degree(direction_vector=multiply(vector=avoidance_direction, scalar=-1))


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
