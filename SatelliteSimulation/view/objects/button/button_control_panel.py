#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Disturbance Buttons for the UI
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pygame

from SatelliteSimulation.controller.shared.disturbance_type import DisturbanceType
from SatelliteSimulation.view.objects.button.pygame_button import Button


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class ButtonControlPanel:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, x: float, y: float, width: float, height_padding: float, font_size: float):
        self.__x: float = x
        self.__y: float = y
        button = Button(x, y, width, font_size, button_text=DisturbanceType.MALFUNCTION.value)
        button_height: float = button.get_height()

        # TODO fix calculating y
        self.__height_padding: float = button_height + height_padding
        self.__buttons = [
            button,
            Button(x, y + self.__height_padding, width, font_size,
                button_text=DisturbanceType.SOLAR_RADIATION.value),
            Button(x, y + self.__height_padding * 2, width, font_size,
                button_text=DisturbanceType.MAGNETIC.value),
            Button(x, y + self.__height_padding * 3, width, font_size,
                button_text=DisturbanceType.GRAVITATIONAL.value)]

        self.__font_size = font_size
        self.__height: float = y + self.__height_padding * 3 + button_height
        self.__width = width



    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_top_button(self) -> Button:
        return self.__buttons[-1]

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def height(self) -> float:
        return self.__height
    @property
    def width(self) -> float:
        return self.__width

    @property
    def font(self) -> float:
        return self.__font_size

    @property
    def height_padding(self) -> float:
        return self.__height_padding

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def draw(self, surface: pygame.Surface):
        for button in self.__buttons:
            button.draw(surface)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def calculate_state(self):
        for button in self.__buttons:
            button.calculate_state()


    def get_new_click_events(self) -> list:
        click_events = []
        for button in self.__buttons:
            if button.new_click_event():
                click_events.append(DisturbanceType(button.get_text()))
        return click_events


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    pass
