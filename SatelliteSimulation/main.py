#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Main module for the satellite simulation. Execute this to start the program.
"""

# =========================================================================== #
#  SECTION: Imports                                                           
# =========================================================================== #
import logging

from controller.controller import Controller

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
    Controller()


# =========================================================================== #
#  SECTION: Main Body                                                         
# =========================================================================== #
if __name__ == '__main__':
    level = logging.DEBUG
    format = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=format)
    main()
    
