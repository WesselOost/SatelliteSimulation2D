# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Class Description
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from SatelliteSimulation.view.objects.button.pygame_button import ButtonType


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class ButtonData:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, button_name: str, button_type: ButtonType, on_click_handler):
        self.__button_name: str = button_name
        self.__button_type: ButtonType = button_type
        self.__on_clicked_handler = on_click_handler


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def button_name(self) -> str:
        return self.__button_name


    @property
    def button_type(self) -> ButtonType:
        return self.__button_type


    @property
    def on_clicked_handler(self):
        return self.__on_clicked_handler
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

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
