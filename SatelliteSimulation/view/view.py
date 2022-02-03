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

from SatelliteSimulation.view import Color
from SatelliteSimulation.view.objects.arrow_view import ArrowView
from SatelliteSimulation.view.images import Images
from SatelliteSimulation.view.navigation_handler import NavigationHandler
from SatelliteSimulation.view.objects.view_references import ReferenceViews
from SatelliteSimulation.view.objects.satellite_observance_border_view import SatelliteObservanceBorderView
from SatelliteSimulation.view.objects.satellite_view import SatelliteView

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

FRAME_RATE = 60
EXPECTED_FRAME_RATE = 60


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class GUI:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, controller, border_width: float, border_height: float, border_padding: float):
        pygame.init()
        pygame.display.set_caption("Satellite simulation")
        self.__ratio: float = border_height / border_width

        self.__minimum_surface_width = border_width / 4.5
        self.__minimum_surface_height = border_height / 4.5

        half_screen_size: tuple = self.create_correct_aspect_ratio_width_height(
            pygame.display.Info().current_w // 2,
            pygame.display.Info().current_h // 2)

        self.__surface: pygame.Surface = pygame.display.set_mode(half_screen_size, pygame.RESIZABLE)
        self.__surface.set_alpha(pygame.SRCALPHA)

        self.__initial_height: int = int(border_height)

        self.__scale_factor: float = self.__surface.get_height() / border_height

        self.__images = Images()
        self.__background_img = self.__images.get_background()
        self.__background_img = pygame.transform.scale(self.__background_img, self.__surface.get_size())

        self.__controller = controller
        self.__navigation_handler = NavigationHandler()

        self.__reference_objects: ReferenceViews = ReferenceViews(border_width, border_height, border_padding)
        self.__satellite_border = self.__reference_objects.border_view(self.__scale_factor)
        self.__disturbance_buttons = self.__reference_objects.button_control_panel(self.__scale_factor)
        self.__earth = self.__reference_objects.earth(self.__scale_factor)
        self.__satellite_mini_border = self.__reference_objects.mini_border_view(self.__scale_factor)

        self.__satellite_observance_line_thickness: float = 4 * self.__scale_factor
        self.__velocity_arrow_default_size: float = 40 * self.__scale_factor

        self.__clock = pygame.time.Clock()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    def get_satellite_border_scale(self) -> float:
        return self.__scale_factor * self.__reference_objects.get_satellite_border_percentage()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def update(self, satellites: list, arrows: list, satellite_observance_borders: list):
        surface = self.__surface

        surface.blit(self.__background_img, (0, 0))
        self.__earth.draw(self.__surface)
        self.__draw_border_connection_lines(surface)
        self.__satellite_border.draw(surface, 2)
        self.__satellite_mini_border.draw(surface, 1)

        self.__disturbance_buttons.draw(surface)

        if satellite_observance_borders:
            for observance_border in satellite_observance_borders:
                self.__draw_satellite_observance_border(observance_border)

        if arrows:
            for arrow in arrows:
                self.__draw_satellite_velocity_arrow(arrow)

        if satellites:
            for satellite in satellites:
                self.__draw_satellite(satellite)

        pygame.display.update()


    def __draw_satellite_velocity_arrow(self, arrow: ArrowView):
        # arrow body
        pygame.draw.line(self.__surface, arrow.color, arrow.end_of_line, arrow.start_of_line, arrow.line_thickness)
        # arrow head
        pygame.draw.polygon(self.__surface, arrow.color, arrow.arrow_head)


    def __draw_satellite_observance_border(self, observance_border: SatelliteObservanceBorderView):
        pygame.draw.circle(self.__surface,
                           observance_border.color,
                           observance_border.position,
                           observance_border.radius,
                           observance_border.line_thickness)


    def __draw_border_connection_lines(self, surface):
        satellite_border = self.__satellite_border.get_border_rectangle()
        satellite_mini_border = self.__satellite_mini_border.get_border_rectangle()
        pygame.draw.aaline(surface, Color.LIGHT_GREY, satellite_border.topleft, satellite_mini_border.topleft, 3)
        pygame.draw.aaline(surface, Color.LIGHT_GREY, satellite_border.bottomleft, satellite_mini_border.bottomleft, 3)
        pygame.draw.aaline(surface, Color.LIGHT_GREY, satellite_border.bottomright, satellite_mini_border.bottomright,
                           3)
        pygame.draw.aaline(surface, Color.LIGHT_GREY, satellite_border.topright, satellite_mini_border.topright, 3)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def create_correct_aspect_ratio_width_height(self, width: int, height: int) -> tuple:
        new_ratio = height / width
        if new_ratio > self.__ratio:
            resize_width = width
            resize_height = round(resize_width * self.__ratio)
        else:
            resize_height = height
            resize_width = round(resize_height / self.__ratio)

        if resize_width < self.__minimum_surface_width:
            resize_width = self.__minimum_surface_width
            resize_height = self.__minimum_surface_height
        return resize_width, resize_height


    def __scale_on_changed(self, scale_factor: float):
        self.__satellite_border = self.__reference_objects.border_view(self.__scale_factor)
        self.__disturbance_buttons = self.__reference_objects.button_control_panel(self.__scale_factor)
        self.__earth = self.__reference_objects.earth(self.__scale_factor)
        self.__satellite_mini_border = self.__reference_objects.mini_border_view(self.__scale_factor)

        self.__satellite_observance_line_thickness *= scale_factor
        self.__velocity_arrow_default_size *= scale_factor


    def __draw_satellite(self, satellite: SatelliteView):
        if satellite.type > 4:
            image = self.__images.get_asteroid()
        else:
            image = self.__images.get_satellite(satellite.type, satellite.is_crashed)

        image = pygame.transform.scale(image, satellite.size)
        self.__surface.blit(image, (satellite.x, satellite.y))


    def calculate_delta_time(self):
        return self.__clock.tick(FRAME_RATE) * .001 * EXPECTED_FRAME_RATE


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__controller.quit()
            self.__navigation_handler.handle_key_events(event)
            if event.type == pygame.VIDEORESIZE:
                self.__surface = pygame.display.set_mode(
                    self.create_correct_aspect_ratio_width_height(event.w, event.h),
                    pygame.RESIZABLE)

                self.__scale_factor = self.__surface.get_height() / self.__initial_height
                self.__scale_on_changed(self.__scale_factor)
                print(self.__background_img.get_size())
                self.__background_img = self.__images.get_background()
                print(self.__background_img.get_size())
                self.__background_img = pygame.transform.scale(self.__background_img, self.__surface.get_size())
                print(self.__background_img.get_size())


    def calculate_button_states_and_handle_click_events(self):
        self.__disturbance_buttons.calculate_state()
        for click_event_text in self.__disturbance_buttons.get_new_click_events():
            self.__controller.create_disturbance(click_event_text)


    def handle_user_navigation(self):
        if self.__navigation_handler.should_navigate():
            pressed_left, pressed_up, pressed_right, pressed_down = self.__navigation_handler.get_button_states()
            self.__controller.navigate_satellite(pressed_left,
                                                 pressed_up,
                                                 pressed_right,
                                                 pressed_down)


    def quit(self):
        pygame.quit()


    def get_satellite_border_margin(self):
        return self.__satellite_border.margin


    def get_satellite_border_padding(self):
        return self.__satellite_border.padding


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    pass
