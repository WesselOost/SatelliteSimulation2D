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
sys.dont_write_bytecode = True
sys.path.append(os.getcwd())

import random
import os
import sys

sys.dont_write_bytecode = True
sys.path.append(os.getcwd())

from SatelliteSimulation.model.disturbance.disturbance_type import DisturbanceType
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
        border: SatelliteBorder = SatelliteBorder(x=0, y=0, width=1920, height=1080, padding=30, margin=40)
        self.space = Space(satellite_amount=15, border=border)

        self.gui = GUI(controller=self,
            border_width=border.width(),
            border_height=border.height())

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
        self.space.avoid_possible_future_collisions()
        self.space.move_satellites()
        self.space.update_satellite_observance()
        self.space.check_and_handle_collisions()
        self.gui.update(self.space.get_satellites())


    def update_scale(self, scale_factor: float):
        self.space.update_border_and_satellite_scale(scale_factor)


    def get_satellite_border(self) -> tuple:
        border = self.space.get_border()
        return border.x(), border.y(), border.width(), border.height(), border.padding()
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
