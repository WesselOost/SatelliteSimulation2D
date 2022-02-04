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

from SatelliteSimulation.view.objects.button.pygame_button import Button, ToggleButton, ButtonType, ButtonState


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class ButtonControlPanelView:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, x: float, y: float, width: float, height_padding: float, font_size: float, button_data: list):
        self.__button_data = button_data
        self.__x: float = x
        self.__y: float = y
        self.__buttons: dict = {}

        # create button and toggle buttons
        for data in button_data:
            name: str = data.button_name
            on_clicked_handler = data.on_clicked_handler
            if data.button_type == ButtonType.TOGGLE_BUTTON:
                self.__buttons[name] = ToggleButton(0, 0, width, font_size, name, on_clicked_handler)
            else:
                self.__buttons[name] = Button(0, 0, width, font_size, name, on_clicked_handler)

        # use the first button to get the height of the button which is needed for spacing the buttons
        first_button: Button = list(self.__buttons.values())[0]
        button_height = first_button.get_height()
        self.__height_padding: float = button_height + height_padding

        # set position
        for index, button_name in enumerate(self.__buttons):
            self.__buttons[button_name].set_position(self.__x, self.__y * (index + 1) + height_padding * index)

        self.__font_size = font_size
        self.__width = width


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    @property
    def x(self) -> float:
        return self.__x


    @property
    def y(self) -> float:
        return self.__y


    @property
    def width(self) -> float:
        return self.__width


    @property
    def font(self) -> float:
        return self.__font_size


    @property
    def height_padding(self) -> float:
        return self.__height_padding


    @property
    def button_data(self) -> list:
        return self.__button_data


    def get_button(self, button_name: str) -> Button:
        return self.__buttons[button_name]


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def draw(self, surface: pygame.Surface):
        for button_name in self.__buttons:
            self.__buttons[button_name].draw(surface)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def calculate_state(self):
        for button_name in self.__buttons:
            self.__buttons[button_name].calculate_state()


    def handle_new_click_events(self):
        for button_name in self.__buttons:
            button = self.__buttons[button_name]
            if button.new_click_event():
                button.activate_click_handler()


    def get_new_click_events(self):

        for button_name in self.__buttons:
            if self.__buttons[button_name].new_click_event():
                self.__buttons[button_name].activate_click_handler()


    def disable(self, button_names: list):
        for button_name in button_names:
            self.__buttons[button_name].disable()


    def enable(self, button_names: list):
        for button_name in button_names:
            self.__buttons[button_name].enable()


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    pass
