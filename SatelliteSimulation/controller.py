#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Link    : link
# @Version : 0.0.1
"""
Controller of the satellite simulation.
"""

# =========================================================================== #
#  SECTION: Imports                                                           
# =========================================================================== #
import random

from model import *
from view import *


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
        self.gui = GUI(controller=self, width=1400, height=800)
        border_parameter = self.gui.get_satellite_border()
        
        self.space = Space(satelliteAmount=random.randint(1,30),
                           border_corner_x=border_parameter[0],
                           border_corner_y=border_parameter[1],
                           border_width=border_parameter[2],
                           border_heigth=border_parameter[3])
        self.gui.start_simulation_loop()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def create_disturbance(self, disturbanceType: str):
        print(disturbanceType)
        self.space.create_disturbance(disturbanceType)

    def next_frame(self):
        self.gui.update(self.space.satellites)

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
