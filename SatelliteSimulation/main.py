#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Version : 1.0.0
"""
Main module for the satellite simulation. Execute this to start the program.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import logging

from SatelliteSimulation.presenter.presenter import Presenter

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #
def main():
    Presenter()


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    # level = logging.INFO
    level = logging.DEBUG
    # level = logging.ERROR
    format = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=format)
    main()

