# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from unittest import TestCase

from SatelliteSimulation.model.basic_math.vector import Vector
from SatelliteSimulation.model.collision.collision_avoidance_handler import calculate_degrees_which_avoids_object_by_90_degrees


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class TestCollisionAvoidanceHandler(TestCase):
    """
    Test class for the CollisionAvoidanceHandler.
    """
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
        self.no_direction = Vector(0, 0)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p1,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p2,
                                                                                observed_object_direction=self.direction_270)
        self.assertAlmostEqual(180, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p3,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p4,
                                                                                observed_object_direction=self.direction_270)
        self.assertAlmostEqual(0, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p5,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p6,
                                                                                observed_object_direction=self.direction_270)
        self.assertAlmostEqual(0, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p7,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p8,
                                                                                observed_object_direction=self.direction_270)
        self.assertAlmostEqual(180, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p1,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p2,
                                                                                observed_object_direction=self.direction_180)
        self.assertAlmostEqual(270, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p3,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p4,
                                                                                observed_object_direction=self.direction_180)
        self.assertAlmostEqual(270, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p5,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p6,
                                                                                observed_object_direction=self.direction_180)
        self.assertAlmostEqual(90, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p7,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p8,
                                                                                observed_object_direction=self.direction_180)
        self.assertAlmostEqual(90, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p1,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p2,
                                                                                observed_object_direction=self.direction_90)
        self.assertAlmostEqual(180, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p3,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p4,
                                                                                observed_object_direction=self.direction_90)
        self.assertAlmostEqual(0, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p5,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p6,
                                                                                observed_object_direction=self.direction_90)
        self.assertAlmostEqual(0, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p7,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p8,
                                                                                observed_object_direction=self.direction_90)
        self.assertAlmostEqual(180, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p1,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p2,
                                                                                observed_object_direction=self.direction_0)
        self.assertAlmostEqual(270, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p3,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p4,
                                                                                observed_object_direction=self.direction_0)
        self.assertAlmostEqual(270, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p5,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p6,
                                                                                observed_object_direction=self.direction_0)
        self.assertAlmostEqual(90, avoidance_degrees, places=2)


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
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p7,
                                                                                satellite_direction=self.no_direction,
                                                                                observed_object_center=self.p8,
                                                                                observed_object_direction=self.direction_0)

        self.assertAlmostEqual(90, avoidance_degrees, places=2)


    def test_avoiding_by_90_degrees_when_no_direction_and_observed_satellite_is_top_right(self):
        """
        GIVEN:
        observed satellite centre is ABOVE and to the RIGHT of the satellites centre
        and the observed satellite is not moving
        and the own direction is 45 degrees
        WHEN:
        the direction should be avoided by 90 degrees away from the observed satellite
        THEN:
        the resulting degrees should be 135
        """
        avoidance_degrees = calculate_degrees_which_avoids_object_by_90_degrees(satellite_center=self.p1,
                                                                                satellite_direction=Vector(1, 1),
                                                                                observed_object_center=self.p2,
                                                                                observed_object_direction=self.no_direction)
        self.assertAlmostEqual(135, avoidance_degrees, places=2)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


