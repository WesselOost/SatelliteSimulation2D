"""
Handles and detects collisions between 2 circles (satellites) and border collisions
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import logging

from model.border import Border
from model.satellite.satellite import Satellite
from model.basic_math.vector import *


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


def check_and_handle_satellite_collisions(satellite: Satellite, satellites: list):
    for other_satellite in satellites:
        # only check for collisions with satellites that are in the observance radius
        if other_satellite in satellite.observed_satellites() and __collision_detected(satellite, other_satellite):
            __satellite_overlap_resolution_by_shifting_both_equally(satellite, other_satellite)
            velocity1_new, velocity2_new = __calculate_new_velocities(satellite, other_satellite)
            __collision_resolution(satellite, velocity1_new)
            __collision_resolution(other_satellite, velocity2_new)


def check_and_handle_border_collisions(border: Border, satellites: list):
    a_satellite_out_of_border = True
    satellite_overlap = True
    max_iterations: int = 20

    while a_satellite_out_of_border and satellite_overlap and max_iterations != 0:
        satellite_overlap = False
        a_satellite_out_of_border = False

        for satellite in satellites:
            if not border.is_object_inside_border(center=satellite.center(), radius=satellite.radius()):
                a_satellite_out_of_border = True
                new_x, new_y = __calculate_new_xy_for_satellite(border, satellite)

                satellite.velocity_handler.clear()

                satellite_overlap = satellite_overlap or \
                                    __handle_satellite_overlap_shifts(x_shift=new_x - satellite.position.x(),
                                                                      y_shift=new_y - satellite.position.y(),
                                                                      satellites=satellites)
        max_iterations -= 1


# =========================================================================== #
#  SECTION: private Function definitions
# =========================================================================== #

def __collision_detected(satellite1: Satellite, satellite2: Satellite) -> bool:
    if __satellites_overlap(satellite1, satellite2):
        return True
    return False


def __satellites_overlap(satellite1: Satellite, satellite2: Satellite) -> bool:
    distance = calculate_distance(satellite1.center(), satellite2.center())
    radius_sum = satellite1.radius() + satellite2.radius()
    if distance <= radius_sum:
        return True
    return False


def __satellite_overlap_resolution_by_shifting_both_equally(satellite1: Satellite, satellite2: Satellite):
    distance: float = calculate_distance(satellite1.center(), satellite2.center())
    radius_sum: float = satellite1.radius() + satellite2.radius()
    half_overlap: float = 0.5 * (distance - radius_sum)

    s1_x: float = satellite1.center().x()
    s2_x: float = satellite2.center().x()
    shift_x: float = (half_overlap * (s1_x - s2_x) / distance)

    s1_y: float = satellite1.center().y()
    s2_y: float = satellite2.center().y()
    shift_y: float = (half_overlap * (s1_y - s2_y) / distance)

    total_shift: Vector = Vector(shift_x, shift_y)

    satellite1.position.add_vector(multiply(total_shift, -1))
    satellite2.position.add_vector(total_shift)


def __calculate_new_velocities(satellite1, satellite2):
    m1: float = satellite1.mass()
    m2: float = satellite2.mass()
    M: float = m1 + m2
    p1: Vector = satellite1.center()
    p2: Vector = satellite2.center()
    v1: Vector = satellite1.velocity_handler.velocity()
    v2: Vector = satellite2.velocity_handler.velocity()

    # Find a normal vector
    n: Vector = subtract(p1, p2)

    # Find unit normal vector
    un: Vector = multiply(n, 1 / n.magnitude())

    # Find unit tangent vector
    ut: Vector = un.tangent()

    # Project velocities onto the unit normal and unit tangent vectors.
    v1n: float = un.dot_product(v1)
    v1t: float = ut.dot_product(v1)
    v2n: float = un.dot_product(v2)
    v2t: float = ut.dot_product(v2)

    # Find new normal velocities
    # v1` = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
    v1n_tag: float = (v1n * (m1 - m2) + 2 * m2 * v2n) / M
    # v2` = (v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)
    v2n_tag: float = (v2n * (m2 - m1) + 2 * m1 * v1n) / M

    # Convert the scalar normal and scalar tangential velocities into vectors
    v1n_tag_vec: Vector = multiply(un, v1n_tag)
    v1t_tag: Vector = multiply(ut, v1t)
    v2n_tag_vec: Vector = multiply(un, v2n_tag)
    v2t_tag: Vector = multiply(ut, v2t)

    # calculate new velocities
    v1_new: Vector = add(v1n_tag_vec, v1t_tag)
    v2_new: Vector = add(v2n_tag_vec, v2t_tag)

    # calculate momentum before and after
    momentum_before: Vector = add(multiply(v1, m1), multiply(v2, m2))
    mag1 = momentum_before.magnitude()
    momentum_after: Vector = add(multiply(v1_new, m1), multiply(v2_new, m2))
    mag2 = momentum_after.magnitude()

    if not math.isclose(mag1, mag2):
        logging.error("impulses not the same")

    return v1_new, v2_new


def __collision_resolution(satellite: Satellite, velocity_new: Vector):
    __set_collision_velocity(satellite, velocity_new)
    satellite.update_crashed_status()
    __add_deceleration(satellite)


def __set_collision_velocity(satellite, velocity_new):
    # subtract the disturbance velocity from the new velocity
    # because the disturbance velocity might increase or decrease next frame.
    collision_velocity: Vector = subtract(velocity_new, satellite.velocity_handler.disturbance_velocity())
    satellite.velocity_handler.collision_velocity().set_vector(collision_velocity)


def __add_deceleration(satellite):
    # duration of the collision deceleration
    t_vertex: int = 20
    satellite.velocity_handler.collision_velocity().solve_equation_and_set_v1_v2(
        satellite.velocity_handler.collision_velocity().magnitude(), t_vertex)
    # start at the velocity tv_max/t_vertex -> only decelerate the velocity
    satellite.velocity_handler.collision_velocity().set_t(t_vertex)


def __calculate_new_xy_for_satellite(border: Border, satellite: Satellite) -> tuple:
    satellite_x = satellite.position.x()
    satellite_size = satellite.size()
    satellite_right_edge = satellite_x + satellite_size

    new_x: float = satellite_x

    if satellite_right_edge > border.right():
        new_x = border.right() - satellite_size

    if satellite_x < border.left():
        new_x = border.left()

    satellite.position.set_x(new_x)

    satellite_y = satellite.position.y()
    satellite_bottom_edge = satellite_y + satellite_size
    new_y: float = satellite_y

    if satellite_y < border.top():
        new_y = border.top()

    if satellite_bottom_edge > border.bottom():
        new_y = border.bottom() - satellite_size

    satellite.position.set_y(new_y)

    return new_x, new_y


def __handle_satellite_overlap_shifts(x_shift, y_shift, satellites: list) -> bool:
    overlap_occurred: bool = False
    for i, sat1 in enumerate(satellites):
        for sat2 in satellites[i + 1:]:

            if __satellites_overlap(sat1, sat2):
                overlap_occurred = True
                __shift_x(sat1, sat2, x_shift)
                __shift_y(sat1, sat2, y_shift)

    return overlap_occurred


def __shift_x(sat1: Satellite, sat2: Satellite, x_shift: float):
    x1 = sat1.position.x()
    x2 = sat2.position.x()
    if __no_shift_or_positions_equal(x1, x2, x_shift):
        pass
    elif __p1_further_from_border_than_p2(x1, x2, x_shift):
        sat1.position.add_to_x(x_shift)
    else:
        sat2.position.add_to_x(x_shift)


def __shift_y(sat1: Satellite, sat2: Satellite, y_shift: float):
    y1 = sat1.position.y()
    y2 = sat2.position.y()
    if __no_shift_or_positions_equal(y1, y2, y_shift):
        pass
    elif __p1_further_from_border_than_p2(y1, y2, y_shift):
        sat1.position.add_to_y(y_shift)
    else:
        sat2.position.add_to_y(y_shift)


def __no_shift_or_positions_equal(p1, p2, shift):
    return shift == 0 or p1 == p2


def __p1_further_from_border_than_p2(p1: float, p2: float, shift: float) -> bool:
    return (shift > 0 and p1 > p2) or (shift < 0 and p1 < p2)

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
