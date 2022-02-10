# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Handles and detects collisions between 2 circles
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from SatelliteSimulation.model.satellite.satellite import Satellite
from SatelliteSimulation.model.basic_math.vector import *

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


def check_and_handle_satellite_collisions(satellite: Satellite, satellites: list):
    for other_satellite in satellites:
        # only check for collisions with satellites that are in the observance radius
        if other_satellite in satellite.observed_satellites() and collision_detected(satellite, other_satellite):
            satellite_overlap_resolution_by_shifting_both_equally(satellite, other_satellite)
            velocity1_new, velocity2_new = calculate_new_velocities(satellite, other_satellite)
            collision_resolution(satellite, velocity1_new)
            collision_resolution(other_satellite, velocity2_new)


def collision_detected(satellite1: Satellite, satellite2: Satellite) -> bool:
    if satellites_overlap(satellite1, satellite2):
        return True
    return False


def satellites_overlap(satellite1: Satellite, satellite2: Satellite) -> bool:
    distance = calculate_distance(satellite1.center(), satellite2.center())
    radius_sum = satellite1.radius() + satellite2.radius()
    if distance <= radius_sum:
        return True
    return False


def satellite_overlap_resolution_by_shifting_both_equally(satellite1: Satellite, satellite2: Satellite):
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


def calculate_new_velocities(satellite1, satellite2):
    m1: float = satellite1.mass()
    m2: float = satellite2.mass()
    M: float = m1 + m2
    p1: Vector = satellite1.center()
    p2: Vector = satellite2.center()
    v1: Vector = satellite1.velocity.value()
    v2: Vector = satellite2.velocity.value()

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


def collision_resolution(satellite: Satellite, velocity_new: Vector):
    set_collision_velocity(satellite, velocity_new)
    satellite.update_crashed_status()
    add_deceleration(satellite)


def set_collision_velocity(satellite, velocity_new):
    # subtract the disturbance velocity from the new velocity
    # because the disturbance velocity might increase or decrease next frame.
    collision_velocity: Vector = subtract(velocity_new, satellite.velocity.disturbance_velocity())
    satellite.velocity.collision_velocity().set_vector(collision_velocity)


def add_deceleration(satellite):
    # duration of the collision deceleration
    t_vertex: int = 20
    satellite.velocity.collision_velocity().solve_equation_and_set_v1_v2(
        satellite.velocity.collision_velocity().magnitude(), t_vertex)
    # start at the velocity tv_max/t_vertex -> only decelerate the velocity
    satellite.velocity.collision_velocity().set_t(t_vertex)


# =========================================================================== #
#  SECTION: private Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
