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
from SatelliteSimulation.model.basic_math.math_basic import StraightLineEquation, LinearSystemOfEquations
from SatelliteSimulation.model.satellite.satellite import Satellite

from SatelliteSimulation.model.basic_math.vector import *

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
from SatelliteSimulation.model.satellite_border import SatelliteBorder


def check_and_handle_satellite_collisions(border: SatelliteBorder, satellite: Satellite, satellites: list):
    for other_satellite in satellites:
        # only check for collisions with satellites that are in the observance radius
        if other_satellite in satellite.observed_satellites() and collision_detected(satellite, other_satellite):
            satellite.update_crashed_status()
            other_satellite.update_crashed_status()
            satellite_overlap_resolution_by_shifting_both_equally(border, satellite, other_satellite)
            collision_resolution(satellite, other_satellite)


def collision_detected(satellite1: Satellite, satellite2: Satellite) -> bool:
    distance = calculate_distance(satellite1.center(), satellite2.center())
    radius_sum = satellite1.radius() + satellite2.radius()
    if distance <= radius_sum and satellites_move_towards_each_other(satellite1, satellite2):
        return True
    return False


def satellite_overlap_resolution_by_shifting_both_equally(border: SatelliteBorder, satellite1: Satellite,
                                                          satellite2: Satellite):
    distance: float = calculate_distance(satellite1.center(), satellite2.center())
    radius_sum: float = satellite1.radius() + satellite2.radius()
    half_overlap: float = 0.5 * (distance - radius_sum)

    satellite1_x: float = satellite1.center().x()
    satellite2_x: float = satellite2.center().x()
    shift_x = (half_overlap * (satellite1_x - satellite2_x) / distance)

    satellite1_y: float = satellite1.center().y()
    satellite2_y: float = satellite2.center().y()
    shift_y = (half_overlap * (satellite1_y - satellite2_y) / distance)

    satellite1_new_position: Vector = add(satellite1.center(), multiply(Vector(shift_x, shift_y), -1))
    satellite2_new_position: Vector = add(satellite2.center(), Vector(shift_x, shift_y))

    satellite1_in_border: bool = border.is_object_inside_border(satellite1_new_position, satellite1.radius())
    satellite2_in_border: bool = border.is_object_inside_border(satellite2_new_position, satellite2.radius())


    if not satellite1_in_border and not satellite2_in_border:
        logging.error("both satellites outside of the border")
    elif not satellite1_in_border and satellite2_in_border:
        print(
            f's1 center {satellite1.center().get_as_tuple()} new position {satellite1_new_position.get_as_tuple()} radius {satellite1.radius()}')

        apply_ratio_border_shift(border, satellite1, satellite1_new_position, satellite2, satellite2_new_position)
    elif satellite1_in_border and not satellite2_in_border:
        print(
            f's2 center {satellite2.center().get_as_tuple()} new position {satellite2_new_position.get_as_tuple()} radius {satellite2.radius()}')
        apply_ratio_border_shift(border, satellite2, satellite2_new_position, satellite1, satellite1_new_position)

    else:
        satellite1_new_position: Vector = add(satellite1.position, multiply(Vector(shift_x, shift_y), -1))
        satellite2_new_position: Vector = add(satellite2.position, Vector(shift_x, shift_y))
        satellite1.position.set_vector(satellite1_new_position)
        satellite2.position.set_vector(satellite2_new_position)


def apply_ratio_border_shift(border, satellite1, satellite1_new_position, satellite2, satellite2_new_position):
    satellite1_trajectory: StraightLineEquation = StraightLineEquation(satellite1.center().get_as_tuple(),
                                                                       satellite1_new_position.get_as_tuple())
    satellite2_trajectory: StraightLineEquation = StraightLineEquation(satellite2.center().get_as_tuple(),
                                                                       satellite2_new_position.get_as_tuple())

    lgs = LinearSystemOfEquations()

    print(f'border({border.x()},{border.y()})')
    border.eq_top().print_equation()
    border.eq_right().print_equation()
    border.eq_left().print_equation()
    border.eq_bottom().print_equation()

    satellite1_trajectory.print_equation()

    intersections: list = [lgs.get_intersection(border.eq_top(), satellite1_trajectory),
                           lgs.get_intersection(border.eq_right(), satellite1_trajectory),
                           lgs.get_intersection(border.eq_bottom(), satellite1_trajectory),
                           lgs.get_intersection(border.eq_left(), satellite1_trajectory)]

    radial_vector: Vector = satellite1_trajectory.calculate_radial_vector(satellite1.radius())
    # radial_vector = multiply(satellite1.center().unit_normal(), satellite1.radius())
    radial_vector2: Vector = satellite2_trajectory.calculate_radial_vector(satellite2.radius())

    print(f'radial vector {radial_vector} mag {radial_vector.magnitude()}')
    for n, intersection in enumerate(intersections):
        print(f'n = {n} intersection {intersection}')
        if intersection != (float('inf'), float('inf')):
            t = satellite1_trajectory.calculate_t(intersection)
            print(f't {t}')
            x_inside_width = border.left() <= intersection[0] <= border.right()
            y_inside_width = border.top() <= intersection[1] <= border.bottom()

            if t >= 0 and x_inside_width and y_inside_width:
                print(f'n= {n} t = {t}, intersection = {intersection})')
                intersection_vector: Vector = Vector(x=intersection[0], y=intersection[1])
                # satellite1_new_position = add(satellite1_new_position, radial_vector)
                # calculate_distance(add(satellite1_new_position, radial_vector), intersection_vector)
                # center_overlap: float = calculate_distance(add(satellite1_new_position, radial_vector), intersection_vector)
                center_overlap: float = calculate_distance(satellite1_new_position, intersection_vector)
                # border_overlap: float = satellite1.radius() + center_overlap
                possible_movement: float = calculate_distance(add(satellite1.center(), radial_vector), intersection_vector)

                unit_normal = satellite1_new_position.unit_normal()
                print(unit_normal)
                print(f'possible movement {possible_movement}')
                print(satellite1)
                satellite1.position.add_vector(multiply(unit_normal, possible_movement))
                print(satellite1)
                print(satellite2)

                # print(f'border overlap {border_overlap}')
                print(f'center overlap {center_overlap}')
                unit_normal2 = satellite2_new_position.unit_normal()
                print(f'unit normal2 {unit_normal2}')
                shift = satellite2_new_position.magnitude() + center_overlap + satellite2.radius()
                print(f'shift{shift}')
                satellite2.position.set_vector(shift)
                print(satellite2)

# from arrow class was just to try out
def shift_vector_by_length(start_position: Vector, direction_vector: Vector, length: float) -> Vector:
    distance: float = calculate_distance(direction_vector, start_position)
    dx_dy: Vector = subtract(direction_vector, start_position)
    unit_normal_direction_vector: Vector = divide(dx_dy, distance)
    scaled_direction_vector: Vector = multiply(unit_normal_direction_vector, length)
    return add(start_position, scaled_direction_vector)

def collision_resolution(satellite1: Satellite, satellite2: Satellite):
    subtracted_position_vector: Vector = subtract(satellite1.center(), satellite2.center())
    unit_normal: Vector = divide(subtracted_position_vector, scalar=subtracted_position_vector.magnitude())

    s1_new_normal_velocity: Vector = __calculate_new_normal_velocity(
        satellite1=satellite1,
        satellite2=satellite2,
        unit_normal=unit_normal)

    s2_new_normal_velocity: Vector = __calculate_new_normal_velocity(
        satellite1=satellite2,
        satellite2=satellite1,
        unit_normal=unit_normal)

    unit_tangent: Vector = unit_normal.tangent()
    s1_new_tangent_velocity: Vector = __calculate_new_tangent_velocity(satellite1, unit_tangent)
    s2_new_tangent_velocity: Vector = __calculate_new_tangent_velocity(satellite2, unit_tangent)

    s1_velocity_result: Vector = add(s1_new_normal_velocity, s1_new_tangent_velocity)
    s2_velocity_result: Vector = add(s2_new_normal_velocity, s2_new_tangent_velocity)

    satellite1.velocity.collision_velocity().set_vector(s1_velocity_result)
    satellite2.velocity.collision_velocity().set_vector(s2_velocity_result)
    t = 20
    satellite1.velocity.collision_velocity().solve_equation_and_set_v1_v2(
        satellite1.velocity.collision_velocity().magnitude(), t)
    satellite1.velocity.collision_velocity().set_t(t // 2)
    satellite2.velocity.collision_velocity().solve_equation_and_set_v1_v2(
        satellite2.velocity.collision_velocity().magnitude(), t)
    satellite2.velocity.collision_velocity().set_t(t // 2)


# =========================================================================== #
#  SECTION: private Function definitions
# =========================================================================== #
def satellites_move_towards_each_other(satellite1: Satellite, satellite2: Satellite) -> bool:
    velocity_subtracted: Vector = subtract(satellite2.velocity.value(), satellite1.velocity.value())
    position_subtracted: Vector = subtract(satellite1.center(), satellite2.center())
    return velocity_subtracted.dot_product(position_subtracted) > 0


def __calculate_new_normal_velocity(satellite1: Satellite, satellite2: Satellite, unit_normal: Vector) -> Vector:
    s1_velocity_dp_normal: float = satellite1.velocity.value().dot_product(unit_normal)
    s2_velocity_dp_normal: float = satellite2.velocity.value().dot_product(unit_normal)

    velocity_new_dp_normal: float = __calculate_new_dot_product_velocity(
        satellite1.mass(),
        satellite2.mass(),
        s1_velocity_dp_normal,
        s2_velocity_dp_normal)
    return multiply(vector=unit_normal, scalar=velocity_new_dp_normal)


def __calculate_new_dot_product_velocity(mass1: float, mass2: float, velocity1_dot_product_normal: float,
                                         velocity2_dot_product_normal: float) -> float:
    """
    FORMULA: v_1n` = (v_1n(m_1 - m_2) + 2m_2 * v_2n) / (m1 + m2)
    :return: normalized value
    """
    return (velocity1_dot_product_normal * (mass1 - mass2) + 2 * mass2 * velocity2_dot_product_normal) / \
           (mass1 + mass2)


def __calculate_new_tangent_velocity(satellite: Satellite, unit_tangent: Vector) -> Vector:
    velocity_dp_tangent: float = satellite.velocity.value().dot_product(unit_tangent)
    return multiply(vector=unit_tangent, scalar=velocity_dp_tangent)


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
