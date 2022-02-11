# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Test class for the CollisionAvoidanceHandler.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from unittest import TestCase

from SatelliteSimulation.model.basic_math.vector import Vector
from SatelliteSimulation.model.collision.collision_avoidance import CollisionAvoidanceHandler
# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class TestCollisionAvoidanceHandler(TestCase):

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def setUp(self) -> None:
        """
                     y
                     ^
            p4       |       p2
               p3    |    p1
                     |
        -------------+-----------> x
                     |
               p5    |    p7
            p6       |       p8
        """
        self.p1 = Vector(2, 2)
        self.p2 = Vector(3, 3)
        self.p3 = Vector(-2, 2)
        self.p4 = Vector(-3, 3)
        self.p5 = Vector(-2, -2)
        self.p6 = Vector(-3, -3)
        self.p7 = Vector(2, -2)
        self.p8 = Vector(3, -3)

        self.direction_0 = Vector(1, 0)
        self.direction_90 = Vector(0, 1)
        self.direction_180 = Vector(-1, 0)
        self.direction_270 = Vector(0, -1)


    def test_avoiding_by_90_degrees_when_direction_270_and_observed_satellite_is_top_right(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the RIGHT of the satellites centre
        and the observed satellite travels at a direction of 270 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 180
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p1,
                                            observed_satellite_center=self.p2,
                                            observed_satellite_direction=self.direction_270)
        self.assertAlmostEqual(180, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_270_and_observed_satellite_is_top_left(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the LEFT of the satellites centre
        and the observed satellite travels at a direction of 270 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 0
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p3,
                                            observed_satellite_center=self.p4,
                                            observed_satellite_direction=self.direction_270)
        self.assertAlmostEqual(0, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_270_and_observed_satellite_is_bottom_left(self):
        """
        GIVEN:
        observed satellite centre is BELLOW and to the LEFT of the satellites centre
        and the observed satellite travels at a direction of 270 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 0
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p5,
                                            observed_satellite_center=self.p6,
                                            observed_satellite_direction=self.direction_270)
        self.assertAlmostEqual(0, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_270_and_observed_satellite_is_bottom_right(self):
        """
        GIVEN:
        observed satellite centre is BELLOW and to the RIGHT of the satellites centre
        and the observed satellite travels at a direction of 270 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 180
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p7,
                                            observed_satellite_center=self.p8,
                                            observed_satellite_direction=self.direction_270)
        self.assertAlmostEqual(180, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_180_and_observed_satellite_is_top_right(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the RIGHT of the satellites centre
        and the observed satellite travels at a direction of 180 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 270
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p1,
                                            observed_satellite_center=self.p2,
                                            observed_satellite_direction=self.direction_180)
        self.assertAlmostEqual(270, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_180_and_observed_satellite_is_top_left(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the LEFT of the satellites centre
        and the observed satellite travels at a direction of 180 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 270
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p3,
                                            observed_satellite_center=self.p4,
                                            observed_satellite_direction=self.direction_180)
        self.assertAlmostEqual(270, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_180_and_observed_satellite_is_bottom_left(self):
        """
        GIVEN:
        observed satellite centre is BELLOW and to the LEFT of the satellites centre
        and the observed satellite travels at a direction of 180 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 90
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p5,
                                            observed_satellite_center=self.p6,
                                            observed_satellite_direction=self.direction_180)
        self.assertAlmostEqual(90, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_180_and_observed_satellite_is_bottom_right(self):
        """
        GIVEN:
        observed satellite centre is BELLOW and to the RIGHT of the satellites centre
        and the observed satellite travels at a direction of 180 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 90
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p7,
                                            observed_satellite_center=self.p8,
                                            observed_satellite_direction=self.direction_180)
        self.assertAlmostEqual(90, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_90_and_observed_satellite_is_top_right(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the RIGHT of the satellites centre
        and the observed satellite travels at a direction of 90 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 180
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p1,
                                            observed_satellite_center=self.p2,
                                            observed_satellite_direction=self.direction_90)
        self.assertAlmostEqual(180, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_90_and_observed_satellite_is_top_left(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the LEFT of the satellites centre
        and the observed satellite travels at a direction of 90 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 0
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p3,
                                            observed_satellite_center=self.p4,
                                            observed_satellite_direction=self.direction_90)
        self.assertAlmostEqual(0, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_90_and_observed_satellite_is_bottom_left(self):
        """
        GIVEN:
        observed satellite centre is BELLOW and to the LEFT of the satellites centre
        and the observed satellite travels at a direction of 90 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 0
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p5,
                                            observed_satellite_center=self.p6,
                                            observed_satellite_direction=self.direction_90)
        self.assertAlmostEqual(0, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_90_and_observed_satellite_is_bottom_right(self):
        """
        GIVEN:
        observed satellite centre is BELLOW and to the RIGHT of the satellites centre
        and the observed satellite travels at a direction of 90 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 180
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p7,
                                            observed_satellite_center=self.p8,
                                            observed_satellite_direction=self.direction_90)
        self.assertAlmostEqual(180, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_0_and_observed_satellite_is_top_right(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the RIGHT of the satellites centre
        and the observed satellite travels at a direction of 0 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 270
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p1,
                                            observed_satellite_center=self.p2,
                                            observed_satellite_direction=self.direction_0)
        self.assertAlmostEqual(270, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_0_and_observed_satellite_is_top_left(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the LEFT of the satellites centre
        and the observed satellite travels at a direction of 0 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 270
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p3,
                                            observed_satellite_center=self.p4,
                                            observed_satellite_direction=self.direction_0)
        self.assertAlmostEqual(270, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_0_and_observed_satellite_is_bottom_left(self):
        """
        GIVEN:
        observed satellite centre is BELLOW and to the LEFT of the satellites centre
        and the observed satellite travels at a direction of 0 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 90
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p5,
                                            observed_satellite_center=self.p6,
                                            observed_satellite_direction=self.direction_0)
        self.assertAlmostEqual(90, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)


    def test_avoiding_by_90_degrees_when_direction_0_and_observed_satellite_is_bottom_right(self):
        """
        GIVEN:
        observed satellite centre is BELLOW and to the RIGHT of the satellites centre
        and the observed satellite travels at a direction of 0 DEGREES
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 90
        """
        handler = CollisionAvoidanceHandler(satellite_center=self.p7,
                                            observed_satellite_center=self.p8,
                                            observed_satellite_direction=self.direction_0)
        self.assertAlmostEqual(90, handler.calculate_degrees_avoiding_satellite_direction_by_90_degrees(), places=2)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


if __name__ == '__main__':
    pass
