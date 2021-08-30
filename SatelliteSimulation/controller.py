#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Link    : link
# @Version : 0.0.1
"""
Short Introduction
"""

# =========================================================================== #
#  SECTION: Imports                                                           
# =========================================================================== #
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
        self.space = Space(satelliteAmount=2)
        self.gui = GUI(controller=self, width=1400, height=800)
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
        # todo remove placeholder satellites
        satelliteA = SatelliteA(400, 100)
        satelliteB = SatelliteB(200, 200)
        satelliteC = SatelliteC(800, 250)
        satellites = [satelliteA, satelliteB, satelliteC]

        self.gui.update(satellites)

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
