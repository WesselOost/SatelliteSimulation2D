#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Link    : link
# @Version : 0.0.1
"""
Short Introduction
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pygame
import os

from model import Satellite
from pygame_button import Button

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
BACKGROUND_COLOR = (0, 0, 0)
FONT_SIZE = 14
FRAMERATE = 60
EARTH_IMG = pygame.image.load(os.path.join(ABSOLUTE_PATH,"Assets", "earth.png"))
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

        ## __private
        self.__surface = pygame.display.set_mode((width, height))
        self.__controller = controller
        self.__earth_img_angle = 0
        self.__simulation_started = False

        offset = height // 10
        self.__init_buttons(offset, width)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def update(self, satellites: list):
        self.__surface.fill(BACKGROUND_COLOR)
        self.rotate_and_draw_earth()

        for satellite in satellites:
            self.__draw_satellite(satellite)

        for button in self.__buttons:
            button.draw(self.__surface)

        pygame.display.update()

    def start_simulation_loop(self):
        if not self.__simulation_started:
            self.__simulation_started = True
            self.__start_simulation_loop()

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #
    def __init_buttons(self, offset, width):
        self.__buttons = [Button(button_text="MAGNETIC DISTURBANCE", font_size=FONT_SIZE),
                          Button(button_text="MALFUNCTION", font_size=FONT_SIZE),
                          Button(button_text="SOLAR RADIATION DISTURBANCE", font_size=FONT_SIZE),
                          Button(button_text="GRAVITY GRADIENT DISTURBANCE", font_size=FONT_SIZE)]

        # todo make buttons same width
        for i, button in enumerate(self.__buttons):
            new_x = width - button.width - offset
            new_y = offset
            if i != 0:
                previous_button = self.__buttons[i - 1]
                new_y += previous_button.y
            button.set_position(new_x, new_y)

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
        image_position = (self.__surface.get_width() - earth_img_rotated.get_width()) // 2, \
                         self.__surface.get_height() - earth_img_rotated.get_height() // 2
        self.__surface.blit(earth_img_rotated, image_position)

    def __draw_satellite(self, satellite: Satellite):
        satellite_img = pygame.image.load(satellite.imgUrl)
        satellite_img = pygame.transform.scale(satellite_img, (satellite.radius, satellite.radius))
        self.__surface.blit(satellite_img, (satellite.x, satellite.y))


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    pass
