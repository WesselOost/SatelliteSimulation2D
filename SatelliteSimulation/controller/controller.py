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

        self.space = Space(satelliteAmount=random.randint(5, 15),
                        border_corner_x=border_parameters[0],
                        border_corner_y=border_parameters[1],
                        border_width=border_parameters[2],
                        border_height=border_parameters[3],
                        border_offset=border_parameters[4])
        self.gui.start_simulation_loop()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def create_disturbance(self, disturbanceType: str):
        self.space.create_disturbance(disturbanceType)


    def next_frame(self):
        satellites_moved: bool = self.space.move_influenced_satellites()
        if satellites_moved:
            self.space.update_satellite_observance()
        self.gui.update(self.space.satellites)


    def update_border_and_satellite_data(self):
        border_corner_x, border_corner_y, border_width, border_height, border_padding = self.gui.get_satellite_border()

        self.space.update_border_and_satellite_data(self.gui.get_scale_factor(),
                                                    border_corner_x=border_corner_x,
                                                    border_corner_y=border_corner_y,
                                                    border_width=border_width,
                                                    border_height=border_height,
                                                    border_padding=border_padding)
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
