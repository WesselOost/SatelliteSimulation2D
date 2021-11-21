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
import logging
import os
import pygame

from SatelliteSimulation.model.basic_math.vector import *
from SatelliteSimulation.model.model import Satellite, SatelliteA, SatelliteB, SatelliteC, SatelliteD
from SatelliteSimulation.model.satellite.satellite import SpaceJunk
from SatelliteSimulation.view import Color
from SatelliteSimulation.view.navigation_handler import NavigationHandler
from SatelliteSimulation.view.disturbance_buttons import DisturbanceButtons
from SatelliteSimulation.view.earth import Earth
from SatelliteSimulation.view.border_view import BorderView

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
DOTTED_CIRCLE_OFFSET = 100

MAX_SURFACE_HEIGHT = 242
MIN_SURFACE_WIDTH = 430
DEFAULT_BUTTON_OFFSET = 50
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FONT_SIZE = 12
FRAME_RATE = 60
BACKGROUND_IMG = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "galaxy_background.jpg"))
SATELLITE_1 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite1.png"))
SATELLITE_2 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite2.png"))
SATELLITE_3 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite3.png"))
SATELLITE_4 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite4.png"))

SATELLITE_1_CRASHED = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite1_crashed.png"))
SATELLITE_2_CRASHED = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite2_crashed.png"))
SATELLITE_3_CRASHED = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite3_crashed.png"))
SATELLITE_4_CRASHED = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite4_crashed.png"))

ASTEROID_1 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "asteroid1.png"))


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class GUI:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, controller, border_width: float, border_height: float):
        pygame.init()
        pygame.display.set_caption("Satellite simulation")
        self.__ratio: float = border_height / border_width

        half_screen_size: tuple = self.create_correct_aspect_ratio_width_height(
            pygame.display.Info().current_w // 2,
            pygame.display.Info().current_h // 2)

        self.__surface: pygame.Surface = pygame.display.set_mode(half_screen_size, pygame.RESIZABLE)
        self.__surface.set_alpha(pygame.SRCALPHA)
        self.initial_height: int = self.__surface.get_height()
        self.__scale_factor: float = (self.initial_height / border_height) * 0.75

        self.image_performance_boost()

        self.__controller = controller
        self.__controller.update_scale(self.__scale_factor)
        self.__navigation_handler = NavigationHandler()

        self.__simulation_started = False

        x, y, width, height, padding = self.__controller.get_satellite_border()
        self.__satellite_border = BorderView(x, y, width, height, padding)
        # self.__satellite_border.show_padding(True)

        border: pygame.Rect = self.__satellite_border.get_border_rectangle()
        self.__disturbance_buttons: DisturbanceButtons = self.__create_disturbance_btns(border)

        self.__earth = Earth(border.center[0], self.__surface, DOTTED_CIRCLE_OFFSET * self.__scale_factor)
        self.__satellite_observance_line_thickness: float = 4 * self.__scale_factor
        self.__velocity_arrow_default_size: float = 40 * self.__scale_factor

        self.__satellite_mini_border = self.__create_mini_border(border, self.__earth.get_dotted_circle_position())


    def image_performance_boost(self):
        BACKGROUND_IMG.convert()
        SATELLITE_1.convert()
        SATELLITE_2.convert()
        SATELLITE_3.convert()
        SATELLITE_4.convert()
        SATELLITE_1_CRASHED.convert()
        SATELLITE_2_CRASHED.convert()
        SATELLITE_3_CRASHED.convert()
        SATELLITE_4_CRASHED.convert()
        ASTEROID_1.convert()


    def __create_disturbance_btns(self, satellite_border: pygame.Rect) -> DisturbanceButtons:
        scaled_button_offset = DEFAULT_BUTTON_OFFSET * self.__scale_factor
        satellite_border_width_and_x = (satellite_border.x + satellite_border.width)
        disturbance_btns_width: float = self.__surface.get_width() - satellite_border_width_and_x - \
                                        (scaled_button_offset * 2)

        disturbance_btns_x: float = satellite_border_width_and_x + scaled_button_offset
        disturbance_btns_y: float = satellite_border.y
        return DisturbanceButtons(x=disturbance_btns_x,
            y=disturbance_btns_y + scaled_button_offset,
            width=disturbance_btns_width,
            padding=scaled_button_offset,
            font_size=FONT_SIZE)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
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
                self.__draw_satellite_observance_border(satellite)

            for satellite in satellites:
                if satellite.velocity.value().magnitude() != 0:
                    self.__draw_satellite_velocity(satellite)

            for satellite in satellites:
                self.__draw_satellite(satellite)
        else:
            # TODO raise Exception
            pass
        self.__disturbance_buttons.draw(surface)

        pygame.display.update()


    def __draw_satellite_velocity(self, satellite):
        arrow = satellite.velocity.arrow()
        # arrow body
        pygame.draw.line(self.__surface, Color.RED, arrow.end_of_line(), arrow.start_of_line(),
            int(arrow.line_thickness()))
        # arrow head
        pygame.draw.polygon(self.__surface, Color.RED,
            [arrow.head_left(), arrow.head_right(), arrow.head_tip()])


    def __draw_satellite_observance_border(self, satellite):
        if not satellite.is_crashed():

            color = Color.ORANGE if satellite.observed_satellites() else Color.GREY
            if satellite.possible_collisions():
                color = Color.RED

            pygame.draw.circle(self.__surface, color, satellite.center().get_as_tuple(),
                satellite.radius() + satellite.observance_radius(),
                max(1, int(self.__satellite_observance_line_thickness)))


    def __draw_border_connection_lines(self, surface):
        satellite_border = self.__satellite_border.get_border_rectangle()
        satellite_mini_border = self.__satellite_mini_border.get_border_rectangle()
        pygame.draw.aaline(surface, Color.LIGHT_GREY, satellite_border.topleft, satellite_mini_border.topleft, 3)
        pygame.draw.aaline(surface, Color.LIGHT_GREY, satellite_border.bottomleft, satellite_mini_border.bottomleft, 3)
        pygame.draw.aaline(surface, Color.LIGHT_GREY, satellite_border.bottomright, satellite_mini_border.bottomright,
            3)
        pygame.draw.aaline(surface, Color.LIGHT_GREY, satellite_border.topright, satellite_mini_border.topright, 3)


    def start_simulation_loop(self):
        if not self.__simulation_started:
            self.__simulation_started = True
            self.__start_simulation_loop()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __create_mini_border(self, satellite_border: pygame.Rect, dotted_circle_position: tuple) -> BorderView:
        mini_border_scale = 0.04
        mini_border_width = satellite_border.width * mini_border_scale
        mini_border_height = satellite_border.height * mini_border_scale
        mini_border_x = satellite_border.center[0] - mini_border_width // 2
        mini_border_y = dotted_circle_position[1] - mini_border_height // 2

        return BorderView(
            x=mini_border_x,
            y=mini_border_y,
            width=mini_border_width,
            height=mini_border_height,
            padding=0
        )


    def __start_simulation_loop(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            delta_time = clock.tick(FRAME_RATE) * .001 * FRAME_RATE

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                self.__navigation_handler.handle_key_events(event)
                if event.type == pygame.VIDEORESIZE:
                    self.__surface = pygame.display.set_mode(
                        self.create_correct_aspect_ratio_width_height(event.w, event.h),
                        pygame.RESIZABLE)

                    self.__scale_factor = self.__surface.get_height() / self.initial_height
                    self.__controller.update_scale(self.__scale_factor)
                    self.__scale_on_changed(self.__scale_factor)
                    self.initial_height = self.__surface.get_height()

            self.__disturbance_buttons.calculate_state()
            for click_event_text in self.__disturbance_buttons.get_new_click_events():
                self.__controller.create_disturbance(click_event_text)
            if self.__navigation_handler.should_navigate():
                pressed_left, pressed_up, pressed_right, pressed_down = self.__navigation_handler.get_button_states()
                self.__controller.navigate_satellite(pressed_left,
                    pressed_up,
                    pressed_right,
                    pressed_down)
            self.__controller.set_delta_time(delta_time)
            self.__controller.next_frame()
        pygame.quit()


    def __navigate_selected_satellite(self):
        pass


    def create_correct_aspect_ratio_width_height(self, width: int, height: int) -> tuple:
        new_ratio = height / width
        if new_ratio > self.__ratio:
            resize_width = width
            resize_height = round(resize_width * self.__ratio)
        else:
            resize_height = height
            resize_width = round(resize_height / self.__ratio)

        if resize_width < MIN_SURFACE_WIDTH:
            resize_width = MIN_SURFACE_WIDTH
            resize_height = MAX_SURFACE_HEIGHT
        return resize_width, resize_height


    def __scale_on_changed(self, scale_factor: float):
        self.__disturbance_buttons.on_size_changed(scale_factor)
        self.__earth.on_size_changed(self.__surface, scale_factor)
        self.__satellite_observance_line_thickness *= scale_factor
        self.__velocity_arrow_default_size *= scale_factor

        x, y, width, height, padding = self.__controller.get_satellite_border()
        self.__satellite_border.update_size(x, y, width, height, padding)
        self.__satellite_mini_border = self.__create_mini_border(self.__satellite_border.get_border_rectangle(),
            self.__earth.get_dotted_circle_position())


    def __draw_satellite(self, satellite: Satellite):
        satellite_img = None
        if isinstance(satellite, SatelliteA):
            if satellite.is_crashed():
                satellite_img = SATELLITE_1_CRASHED
            else:
                satellite_img = SATELLITE_1
        elif isinstance(satellite, SatelliteB):
            if satellite.is_crashed():
                satellite_img = SATELLITE_2_CRASHED
            else:
                satellite_img = SATELLITE_2
        elif isinstance(satellite, SatelliteC):
            if satellite.is_crashed():
                satellite_img = SATELLITE_3_CRASHED
            else:
                satellite_img = SATELLITE_3
        elif isinstance(satellite, SatelliteD):
            if satellite.is_crashed():
                satellite_img = SATELLITE_4_CRASHED
            else:
                satellite_img = SATELLITE_4
        elif isinstance(satellite, SpaceJunk):
            satellite_img = ASTEROID_1
        satellite_img = pygame.transform.scale(satellite_img, (satellite.size(), satellite.size()))

        self.__surface.blit(satellite_img, (satellite.position.x(), satellite.position.y()))


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
