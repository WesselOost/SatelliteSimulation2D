#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
View of the satellite simulation. Everything that is part of the visible GUI
is implemented here. The GUI is based on the python library "pygame".
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pygame
import os

from SatelliteSimulation.view.disturbance_buttons import DisturbanceButtons
from SatelliteSimulation.view.earth import Earth
from SatelliteSimulation.model.model import Satellite, SatelliteA, SatelliteB, SatelliteC, SatelliteD

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
from SatelliteSimulation.view.satellite_border import Border

DEFAULT_BORDER_OFFSET = 30
DEFAULT_BUTTON_OFFSET = 40
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LIGHT_GREY = (243, 243, 243)
FONT_SIZE = 8
FRAME_RATE = 60
BACKGROUND_IMG = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "galaxy_background.jpg"))
SATELLITE_1 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite1.png"))
SATELLITE_2 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite2.png"))
SATELLITE_3 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite3.png"))
SATELLITE_4 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite4.png"))

SATELLITE_1_CRASHED = pygame.image.load(os.path.join(
    ABSOLUTE_PATH, "Assets", "satellite1_crashed.png"))
SATELLITE_2_CRASHED = pygame.image.load(os.path.join(
    ABSOLUTE_PATH, "Assets", "satellite2_crashed.png"))
SATELLITE_3_CRASHED = pygame.image.load(os.path.join(
    ABSOLUTE_PATH, "Assets", "satellite3_crashed.png"))
SATELLITE_4_CRASHED = pygame.image.load(os.path.join(
    ABSOLUTE_PATH, "Assets", "satellite4_crashed.png"))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class GUI:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, controller, width: int, height: int):
        pygame.init()
        pygame.display.set_caption("Satellite simulation")
        self.__ratio = height / width

        half_screen_size = self.create_correct_aspect_ratio_width_height(pygame.display.Info().current_w // 2,
                                                                         pygame.display.Info().current_h // 2)

        self.__surface = pygame.display.set_mode(half_screen_size, pygame.RESIZABLE)

        self.previous_height = self.__surface.get_height()
        self.__scale_factor = 1

        # performance boost
        BACKGROUND_IMG.convert()
        SATELLITE_1.convert()
        SATELLITE_2.convert()
        SATELLITE_3.convert()
        SATELLITE_4.convert()
        SATELLITE_1_CRASHED.convert()
        SATELLITE_2_CRASHED.convert()
        SATELLITE_3_CRASHED.convert()
        SATELLITE_4_CRASHED.convert()

        self.__controller = controller

        self.__simulation_started = False

        self.__disturbance_buttons = DisturbanceButtons(
            DEFAULT_BUTTON_OFFSET,
            self.__surface.get_width(),
            self.__surface.get_height(),
            FONT_SIZE)

        top_button = self.__disturbance_buttons.get_top_button()

        self.__earth = Earth(self.__surface, DEFAULT_BUTTON_OFFSET,
                             earth_offset_x=(self.__surface.get_width() - top_button.x) // 2)

        self.__satellite_border = Border(x=0, y=0, width=top_button.x,
                                        height=top_button.y, margin=DEFAULT_BORDER_OFFSET, padding=DEFAULT_BORDER_OFFSET / 3)
        self.__satellite_border.show_offset()
        self.__satellite_mini_border = self.__create_mini_border(
            self.__satellite_border.get_border(),
            self.__earth.get_dotted_circle_position(),
            self.__earth.get_dotted_circle_width()
        )


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_satellite_border(self) -> tuple:
        border = self.__satellite_border.get_border()
        return border.x, \
                border.y, \
                border.width, \
                border.height, \
                self.__satellite_border.get_padding()


    def get_scale_factor(self) -> float:
        return self.__scale_factor


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def update(self, satellites: list):
        surface = self.__surface

        surface.blit(BACKGROUND_IMG, (0, 0))
        self.__earth.draw()
        self.__draw_border_connection_lines(surface)
        self.__satellite_border.draw(surface, 2)
        self.__satellite_mini_border.draw(surface, 1)

        if satellites:
            for satellite in satellites:
                self.__draw_satellite(satellite)
        else:
            # TODO raise Exception
            print()
        self.__disturbance_buttons.draw(surface)

        pygame.display.update()


    def __draw_border_connection_lines(self, surface):
        satellite_border = self.__satellite_border.get_border()
        satellite_mini_border = self.__satellite_mini_border.get_border()
        pygame.draw.aaline(surface, LIGHT_GREY, satellite_border.topleft, satellite_mini_border.topleft, 3)
        pygame.draw.aaline(surface, LIGHT_GREY, satellite_border.bottomleft, satellite_mini_border.bottomleft, 3)
        pygame.draw.aaline(surface, LIGHT_GREY, satellite_border.bottomright, satellite_mini_border.bottomright, 3)
        pygame.draw.aaline(surface, LIGHT_GREY, satellite_border.topright, satellite_mini_border.topright, 3)


    def start_simulation_loop(self):
        if not self.__simulation_started:
            self.__simulation_started = True
            self.__start_simulation_loop()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __create_mini_border(self, satellite_border: pygame.Rect, dotted_circle_position: tuple,
                            dotted_circle_width: int) -> Border:
        mini_border_scale = 0.04
        mini_border_width = satellite_border.width * mini_border_scale
        mini_border_height = satellite_border.height * mini_border_scale
        mini_border_x = dotted_circle_position[0] + dotted_circle_width // 2 - mini_border_width // 2
        mini_border_y = dotted_circle_position[1] - mini_border_height // 2

        return Border(x=mini_border_x,
                    y=mini_border_y,
                    width=mini_border_width,
                    height=mini_border_height,
                    margin=0,
                    padding=0)


    def __start_simulation_loop(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FRAME_RATE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.VIDEORESIZE:
                    self.__surface = pygame.display.set_mode(
                        self.create_correct_aspect_ratio_width_height(event.w, event.h),
                        pygame.RESIZABLE)

                    self.__scale_factor = self.__surface.get_height() / self.previous_height
                    self.__scale_on_changed(self.__scale_factor)
                    self.previous_height = self.__surface.get_height()
                    self.__controller.update_border_and_satellite_data()
            self.__disturbance_buttons.calculate_state()
            for click_event_text in self.__disturbance_buttons.get_new_click_events():
                self.__controller.create_disturbance(click_event_text)

            self.__controller.next_frame()
        pygame.quit()


    def create_correct_aspect_ratio_width_height(self, width: int, height: int) -> tuple:
        new_ratio = height / width
        if new_ratio > self.__ratio:
            resize_width = width
            resize_height = round(resize_width * self.__ratio)
        else:
            resize_height = height
            resize_width = round(resize_height / self.__ratio)
        return resize_width, resize_height


    def __scale_on_changed(self, scale_factor: float):
        self.__disturbance_buttons.on_size_changed(scale_factor)
        self.__earth.on_size_changed(self.__surface, scale_factor)
        self.__satellite_border.on_size_changed(scale_factor)
        self.__satellite_mini_border.on_size_changed(scale_factor)


    def __draw_satellite(self, satellite: Satellite):
        satellite_img = None
        if isinstance(satellite, SatelliteA):
            if satellite.isCrashed:
                satellite_img = SATELLITE_1_CRASHED
            else:
                satellite_img = SATELLITE_1
        elif isinstance(satellite, SatelliteB):
            if satellite.isCrashed:
                satellite_img = SATELLITE_2_CRASHED
            else:
                satellite_img = SATELLITE_2
        elif isinstance(satellite, SatelliteC):
            if satellite.isCrashed:
                satellite_img = SATELLITE_3_CRASHED
            else:
                satellite_img = SATELLITE_3
        elif isinstance(satellite, SatelliteD):
            if satellite.isCrashed:
                satellite_img = SATELLITE_4_CRASHED
            else:
                satellite_img = SATELLITE_4
        satellite_img = pygame.transform.scale(satellite_img, (satellite.size, satellite.size))
        self.__surface.blit(satellite_img, (satellite.x, satellite.y))


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
