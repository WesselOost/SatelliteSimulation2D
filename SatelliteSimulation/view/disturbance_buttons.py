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

from SatelliteSimulation.model.disturbance.disturbance_type import DisturbanceType
#TODO don't import anything from model
from SatelliteSimulation.view.pygame_button import Button

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #



class DisturbanceButtons:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, offset: int, width: int, height: int, font_size: int):
        self.__buttons = [
            Button(button_text=DisturbanceType.GRAVITATIONAL.value, font_size=font_size),
            Button(button_text=DisturbanceType.SOLAR_RADIATION.value, font_size=font_size),
            Button(button_text=DisturbanceType.MAGNETIC.value, font_size=font_size),
            Button(button_text=DisturbanceType.MALFUNCTION.value, font_size=font_size)]
        self.__font_size = font_size

        self.__init_button_size_and_position(width, height, offset)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_top_button(self) -> Button:
        return self.__buttons[-1]


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def draw(self, surface: pygame.Surface):
        for button in self.__buttons:
            button.draw(surface)


    def on_size_changed(self, scale_factor):
        for button in self.__buttons:
            button.on_size_changed(scale_factor)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __init_button_size_and_position(self, width: int, height: int, offset: int):
        max_button_width = max(button.get_width() for button in self.__buttons)
        new_button_x = width - max_button_width - offset // 2
        for i, button in enumerate(self.__buttons):
            button.set_width(max_button_width)
            new_button_y = (height - offset) if i == 0 else (self.__buttons[i - 1].y - offset)
            button.set_position(new_button_x, new_button_y)


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
