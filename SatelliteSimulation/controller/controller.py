#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Controller of the satellite simulation.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import os
import sys

from SatelliteSimulation.model.arrow import Arrow
from SatelliteSimulation.model.basic_math.vector import multiply, Vector, add
from SatelliteSimulation.model.satellite.satellite import Satellite
from SatelliteSimulation.view import Color
from SatelliteSimulation.view.objects.arrow_view import ArrowView
from SatelliteSimulation.view.objects.satellite_observance_border_view import SatelliteObservanceBorderView
from SatelliteSimulation.view.objects.satellite_view import SatelliteView

sys.dont_write_bytecode = True
sys.path.append(os.getcwd())

import os
import sys

sys.dont_write_bytecode = True
sys.path.append(os.getcwd())

from SatelliteSimulation.controller.shared.disturbance_type import DisturbanceType
from SatelliteSimulation.model.model import Space
from SatelliteSimulation.model.satellite_border import SatelliteBorder
from SatelliteSimulation.view.view import GUI


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class Controller:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self):
        self.__border: SatelliteBorder = SatelliteBorder(x=0, y=0, width=1920, height=1080, padding=30)

        self.space = Space(satellite_amount=15, border=self.__border)

        self.gui = GUI(controller=self,
                       border_width=self.__border.width(),
                       border_height=self.__border.height(),
                       border_padding=self.__border.padding())

        self.__run = True
        self.start_simulation_loop()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def start_simulation_loop(self):
        while self.__run:
            self.set_delta_time(self.gui.calculate_delta_time())
            self.gui.handle_events()
            self.gui.calculate_button_states_and_handle_click_events()
            self.gui.handle_user_navigation()
            self.next_frame()
        self.gui.quit()


    def quit(self):
        self.__run = False


    def create_disturbance(self, disturbanceType: DisturbanceType):
        self.space.create_disturbance(disturbanceType)


    def navigate_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        self.space.navigate_satellite(pressed_left, pressed_up, pressed_right, pressed_down)


    def set_delta_time(self, delta_time: float):
        self.space.set_delta_time(delta_time)


    def next_frame(self):
        scale_factor: float = self.gui.get_satellite_border_scale()
        self.space.avoid_possible_future_collisions()
        self.space.move_satellites()
        satellites: list = self.space.get_satellites()
        self.space.update_satellite_observance()
        self.space.check_and_handle_collisions()

        offset: float = self.gui.get_satellite_border_margin() + self.gui.get_satellite_border_padding()
        arrows: list = [arrow_to_arrow_view(arrow, scale_factor, offset) for arrow in self.space.get_velocity_arrows()]
        satellite_views: list = [satellite_to_satellite_view(satellite, scale_factor, offset) for satellite in
                                 satellites]
        satellite_borders: list = [satellite_to_observance_border_view(satellite, scale_factor, offset) for satellite in
                                   satellites if not satellite.is_crashed()]

        self.gui.update(satellite_views, arrows, satellite_borders)


    def get_satellite_border(self) -> tuple:
        border = self.space.get_border()
        return border.x(), border.y(), border.width(), border.height(), border.padding()

        # ----------------------------------------------------------------------- #
        #  SUBSECTION: Private Methods
        # ----------------------------------------------------------------------- #

        # =========================================================================== #
        #  SECTION: Function definitions
        # =========================================================================== #


def arrow_to_arrow_view(arrow: Arrow, scale_factor: float, offset: float) -> ArrowView:
    arrow_offset: Vector = Vector(offset, offset)
    return ArrowView(start_of_line=add(multiply(arrow.start_of_line(), scale_factor), arrow_offset).get_as_tuple(),
                     end_of_line=add(multiply(arrow.end_of_line(), scale_factor), arrow_offset).get_as_tuple(),
                     arrow_head=[add(multiply(arrow.head_left(), scale_factor), arrow_offset).get_as_tuple(),
                                 add(multiply(arrow.head_right(), scale_factor), arrow_offset).get_as_tuple(),
                                 add(multiply(arrow.head_tip(), scale_factor), arrow_offset).get_as_tuple()],
                     line_thickness=max(1, int(arrow.line_thickness() * scale_factor)))


def satellite_to_satellite_view(satellite: Satellite, scale_factor: float, offset: float) -> SatelliteView:
    x = (scale_factor * satellite.position.x()) + offset
    y = (scale_factor * satellite.position.y()) + offset
    return SatelliteView(x,
                         y,
                         int(scale_factor * satellite.size()),
                         satellite.is_crashed(),
                         satellite.get_type())


def satellite_to_observance_border_view(satellite: Satellite, scale_factor: float,
                                        offset: float) -> SatelliteObservanceBorderView:
    color = Color.ORANGE if satellite.observed_satellites() else Color.GREY
    if satellite.possible_collisions():
        color = Color.RED
    line_thickness: int = max(1, int(SatelliteObservanceBorderView.DEFAULT_LINE_THICKNESS * scale_factor))

    return SatelliteObservanceBorderView(color=color,
                                         position=add(multiply(satellite.center(), scale_factor),
                                                      Vector(offset, offset)).get_as_tuple(),
                                         radius=(satellite.radius() + satellite.observance_radius()) * scale_factor,
                                         line_thickness=line_thickness)

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


if __name__ == '__main__':
    pass
