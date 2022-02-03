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


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
import pygame

from SatelliteSimulation.view.border_view import BorderView
from SatelliteSimulation.view.disturbance_buttons import DisturbanceButtons
from SatelliteSimulation.view.earth import Earth

BORDER_PERCENTAGE = 0.75
MARGIN_PERCENTAGE = 0.01
MINI_BORDER_SCALE = 0.04
FONT_SIZE = 24
DEFAULT_BUTTON_OFFSET = 50


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class ReferenceViews:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, width: float, height: float, padding: float):
        # create border view
        border_view_width: float = width * BORDER_PERCENTAGE
        border_view_height: float = height * BORDER_PERCENTAGE
        border_padding: float = padding * BORDER_PERCENTAGE
        margin: float = width * MARGIN_PERCENTAGE
        self.__border: BorderView = BorderView(0, 0, border_view_width, border_view_height, margin, border_padding)

        # create button controls
        border_as_rectangle: pygame.Rect = self.__border.get_border_rectangle()
        left_over_width: float = width - border_as_rectangle.width - border_as_rectangle.x
        button_width: float = left_over_width - (margin * 5)
        button_x: float = (width - left_over_width) + margin * 3
        button_y: float = border_as_rectangle.y + margin
        self.__disturbance_buttons: DisturbanceButtons = DisturbanceButtons(button_x,
                                                                            button_y,
                                                                            button_width,
                                                                            height_padding=margin,
                                                                            font_size=button_width * 0.05)

        # create earth
        border_center_x: float = border_as_rectangle.center[0]
        left_over_height: float = height - border_as_rectangle.height - border_as_rectangle.y
        earth_size: float = left_over_height
        dotted_circle_padding: float = (left_over_height - (earth_size / 2)) * .5
        self.__earth: Earth = Earth(border_center_x, height, earth_size, dotted_circle_padding)

        # create mini border
        mini_border_width = border_as_rectangle.width * MINI_BORDER_SCALE
        mini_border_height = border_as_rectangle.height * MINI_BORDER_SCALE
        mini_border_x = border_center_x - mini_border_width // 2
        mini_border_y = self.__earth.get_dotted_circle_position()[1] - mini_border_height // 2

        self.__mini_border: BorderView = BorderView(mini_border_x,
                                                    mini_border_y,
                                                    mini_border_width,
                                                    mini_border_height,
                                                    margin=0,
                                                    padding=0)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def get_satellite_border_percentage(self) -> float:
        return BORDER_PERCENTAGE


    def border_view(self, scale_factor: float) -> BorderView:
        return self.__scale_border_view(self.__border, scale_factor)


    def mini_border_view(self, scale_factor: float) -> BorderView:
        return self.__scale_border_view(self.__mini_border, scale_factor)


    def button_control_panel(self, scale_factor: float) -> DisturbanceButtons:
        button_control_panel: DisturbanceButtons = self.__disturbance_buttons
        x: float = button_control_panel.x * scale_factor
        y: float = button_control_panel.y * scale_factor
        width: float = button_control_panel.width * scale_factor
        padding: float = button_control_panel.height_padding * scale_factor
        font_size: float = button_control_panel.font * scale_factor

        return DisturbanceButtons(x, y, width, padding, font_size)


    def earth(self, scale_factor: float) -> Earth:
        earth: Earth = self.__earth
        center_x: float = earth.center_x * scale_factor
        surface_height: float = earth.surface_height * scale_factor
        earth_size: float = earth.earth_size * scale_factor
        dotted_circle_padding: float = earth.dotted_circle_padding * scale_factor
        return Earth(center_x, surface_height, earth_size, dotted_circle_padding)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __scale_border_view(self, border: BorderView, scale_factor):
        border_as_rectangle: pygame.Rect = border.get_border_rectangle()
        x: float = border_as_rectangle.x * scale_factor
        y: float = border_as_rectangle.y * scale_factor
        width: float = border_as_rectangle.width * scale_factor
        height: float = border_as_rectangle.height * scale_factor
        margin: float = border.margin * scale_factor
        padding: float = border.padding * scale_factor
        return BorderView(x, y, width, height, margin, padding)

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


if __name__ == '__main__':
    pass
