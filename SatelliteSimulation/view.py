#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
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

from model import Satellite, SatelliteA, SatelliteB, SatelliteC
from pygame_button import Button

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
BLACK = (0, 0, 0)
LIGHT_GREY = (243, 243, 243)
FONT_SIZE = 14
FRAMERATE = 60
BACKGROUND_IMG = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "galaxy_background.jpg"))
EARTH_IMG = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "earth.png"))
DOTTED_CIRCLE = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "dashed_circle.png"))

SATELLITE_1 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite1.png"))
SATELLITE_2 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite2.png"))
SATELLITE_3 = pygame.image.load(os.path.join(ABSOLUTE_PATH, "Assets", "satellite3.png"))
EARTH_SCALE = 0.4


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

        self.__surface = pygame.display.set_mode((width, height))
        # performance boost
        BACKGROUND_IMG.convert()
        EARTH_IMG.convert()
        DOTTED_CIRCLE.convert()
        SATELLITE_1.convert()
        SATELLITE_2.convert()
        SATELLITE_3.convert()

        self.__controller = controller
        self.__earth_img_angle = 0
        self.__simulation_started = False

        offset = height // 10
        self.__init_buttons(offset, width, height)
        top_button = self.__buttons[-1]
        self.__earth_offset_x = (width - top_button.x) // 2

        size = int(EARTH_IMG.get_width() * EARTH_SCALE) + offset
        self.__dotted_circle = pygame.transform.scale(DOTTED_CIRCLE, (size, size))
        self.__dotted_circle_x = width - top_button.x
        self.__dotted_circle_y = height - (size // 2)

        border_width = (top_button.x - offset * 2)
        border_height = (top_button.y - offset)
        self.__satellite_border = pygame.Rect(offset,  # x
                                              offset,  # y
                                              border_width,
                                              border_height)

        mini_border_scale = 0.04
        mini_border_width = border_width * mini_border_scale
        mini_border_height = border_height * mini_border_scale
        mini_border_x = self.__dotted_circle_x + self.__dotted_circle.get_width() // 2 - mini_border_width // 2
        mini_border_y = self.__dotted_circle_y - mini_border_height // 2
        self.__satellite_mini_border = pygame.Rect(mini_border_x,
                                                   mini_border_y,
                                                   mini_border_width,
                                                   mini_border_height)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_satellite_border(self) -> tuple:
        return self.__satellite_border.x, \
               self.__satellite_border.y, \
               self.__satellite_border.width, \
               self.__satellite_border.height


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def update(self, satellites: list):
        surface = self.__surface

        surface.blit(BACKGROUND_IMG, (0, 0))
        self.rotate_and_draw_earth()

        satellite_border = self.__satellite_border
        satellite_mini_border = self.__satellite_mini_border
        pygame.draw.aaline(surface, LIGHT_GREY, satellite_border.topleft, satellite_mini_border.topleft, 3)
        pygame.draw.aaline(surface, LIGHT_GREY, satellite_border.bottomleft, satellite_mini_border.bottomleft, 3)
        pygame.draw.aaline(surface, LIGHT_GREY, satellite_border.bottomright, satellite_mini_border.bottomright, 3)
        pygame.draw.aaline(surface, LIGHT_GREY, satellite_border.topright, satellite_mini_border.topright, 3)

        surface.blit(self.__dotted_circle, (self.__dotted_circle_x, self.__dotted_circle_y))

        pygame.draw.rect(surface, LIGHT_GREY, satellite_border, 3)
        pygame.draw.rect(surface, BLACK, satellite_border)
        pygame.draw.rect(surface, BLACK, satellite_mini_border)
        pygame.draw.rect(surface, LIGHT_GREY, satellite_mini_border, 1)

        if satellites:
            for satellite in satellites:
                self.__draw_satellite(satellite)
        else:
            # TODO raise Exception
            print()

        for button in self.__buttons:
            button.draw(surface)
        pygame.display.update()


    def start_simulation_loop(self):
        if not self.__simulation_started:
            self.__simulation_started = True
            self.__start_simulation_loop()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __init_buttons(self, offset, width, height):
        self.__buttons = [Button(button_text="GRAVITY GRADIENT DISTURBANCE", font_size=FONT_SIZE),
                          Button(button_text="SOLAR RADIATION DISTURBANCE", font_size=FONT_SIZE),
                          Button(button_text="MAGNETIC DISTURBANCE", font_size=FONT_SIZE),
                          Button(button_text="MALFUNCTION", font_size=FONT_SIZE)]

        max_button_width = max(button.get_width() for button in self.__buttons)
        new_button_x = width - max_button_width - offset // 2

        for i, button in enumerate(self.__buttons):
            button.set_width(max_button_width)
            new_button_y = (height - offset) if i == 0 else (self.__buttons[i - 1].y - offset)
            button.set_position(new_button_x, new_button_y)


    def __start_simulation_loop(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FRAMERATE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for button in self.__buttons:
                button.calculate_state()
                if button.new_click_event():
                    self.__controller.create_disturbance(button.get_text())

            self.__controller.next_frame()
        pygame.quit()


    def rotate_and_draw_earth(self):
        self.__earth_img_angle -= 0.2
        earth_img_rotated = pygame.transform.rotozoom(EARTH_IMG, self.__earth_img_angle, EARTH_SCALE)
        image_position = (self.__surface.get_width() - earth_img_rotated.get_width()) // 2 - self.__earth_offset_x, \
                         self.__surface.get_height() - earth_img_rotated.get_height() // 2
        self.__surface.blit(earth_img_rotated, image_position)


    def __draw_satellite(self, satellite: Satellite):
        satellite_img = None
        if type(satellite) is SatelliteA:
            satellite_img = SATELLITE_1
        if type(satellite) is SatelliteB:
            satellite_img = SATELLITE_2
        if type(satellite) is SatelliteC:
            satellite_img = SATELLITE_3
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
