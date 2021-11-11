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
import random

from SatelliteSimulation.model.satellite_border import SatelliteBorder
from SatelliteSimulation.model.disturbance.disturbance_type import DisturbanceType
from SatelliteSimulation.model.model import Space
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
        self.gui = GUI(controller=self, width=1920, height=1080)
        border_parameters = self.gui.get_satellite_border()
        border: SatelliteBorder = SatelliteBorder(
            x=border_parameters[0],
            y=border_parameters[1],
            width=border_parameters[2],
            height=border_parameters[3],
            padding=border_parameters[4])

        self.space = Space(satellite_amount=random.randint(10, 10), border=border)
        self.gui.start_simulation_loop()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def create_disturbance(self, disturbanceType: DisturbanceType):
        self.space.create_disturbance(disturbanceType)


    def navigate_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        self.space.navigate_satellite(pressed_left, pressed_up, pressed_right, pressed_down)

    def set_delta_time(self, delta_time: float):
        self.space.set_delta_time(delta_time)

    def next_frame(self):
        self.space.avoid_possible_future_collisions()
        self.space.move_satellites()
        self.space.update_satellite_observance()
        self.space.check_and_handle_collisions()
        self.gui.update(self.space.get_satellites())


    def update_scale(self):
        self.space.update_border_and_satellite_scale(self.gui.get_scale_factor())
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
