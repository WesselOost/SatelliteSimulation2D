# !/usr/bin/env python
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

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

RELEASED = "released"
HOVERED = "hovered"
PRESSED = "pressed"

LIGHT_GREY = (243, 243, 243)
LIGHT_BLUE = (121, 155, 194)
BLUE = (38, 81, 121)
GREEN = (132, 194, 172)
TRANSPARENT = (0, 0, 0, 0)


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #

class Button:

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, button_text: str, font_size: int, x=0, y=0):
        self.__state = "released"
        self.__new_click_event = False

        # init button text
        font = pygame.font.SysFont("Verdana", font_size)
        antialias = True
        self.__text = button_text
        self.__text_surface = font.render(button_text, antialias, LIGHT_GREY)
        offset = self.__text_surface.get_height()
        self.__text_offset = offset // 2

        self.width = self.__text_surface.get_width() + offset
        self.x = x
        self.y = y

        # init button body
        self.__body_height = self.__text_surface.get_height() + offset
        self.__body = pygame.Rect(x, y, self.width, self.__body_height)

        # init button border
        self.__bottom_border_height = self.__body_height / 8
        self.__bottom_border_color = LIGHT_BLUE
        self.__bottom_border = pygame.Rect(x, self.__body_height + y, self.width, self.__bottom_border_height)

        self.height = self.__body_height + self.__bottom_border_height

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def set_position(self, new_x: int, new_y: int):
        self.x = new_x
        self.y = new_y
        self.__body.x = new_x
        self.__body.y = new_y
        self.__bottom_border.x = new_x
        self.__bottom_border.y = new_y + self.__body_height

    def get_text(self) -> str:
        return self.__text

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def draw(self, surface: pygame.Surface):
        self.__draw_bottom_border(surface)
        self.__draw_body(surface)
        self.__draw_text(surface)

    def calculate_state(self):
        mouse_position = pygame.mouse.get_pos()
        self.__new_click_event = False

        if self.__pressed_and_state_is_hovered(mouse_position):
            self.__set_state(PRESSED, (self.__body.y + self.__bottom_border_height), TRANSPARENT)
            self.__new_click_event = True
        elif self.__hovered_and_state_changed(mouse_position):
            self.__set_state(HOVERED, self.y, GREEN)
        elif self.__released_and_state_changed(mouse_position):
            self.__set_state(RELEASED, self.y, LIGHT_BLUE)

    def new_click_event(self) -> bool:
        return self.__new_click_event

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __set_state(self, state: str, body_y: int, border_color: tuple):
        self.__state = state
        self.__body.y = body_y
        self.__bottom_border_color = border_color

    def __draw_bottom_border(self, surface):
        pygame.draw.rect(surface, self.__bottom_border_color, self.__bottom_border)

    def __draw_body(self, surface):
        corner_arch = self.__body_height // 4
        pygame.draw.rect(surface, BLUE, self.__body, 0, 0, corner_arch, corner_arch)

    def __draw_text(self, surface):
        surface.blit(self.__text_surface, (self.x + self.__text_offset, self.__body.y + self.__text_offset))

    def __pressed_and_state_is_hovered(self, mouse_position) -> bool:
        return self.__mouse_collide_with_button(mouse_position) and \
               self.__mouse_pressed() and \
               self.__state == HOVERED

    def __hovered_and_state_changed(self, mouse_position) -> bool:
        return self.__mouse_collide_with_button(mouse_position) and \
               not self.__mouse_pressed() and \
               self.__state != HOVERED

    def __released_and_state_changed(self, mouse_position) -> bool:
        return not self.__mouse_collide_with_button(mouse_position) and \
               not self.__mouse_pressed() \
               and self.__state != RELEASED

    def __mouse_collide_with_button(self, mouse_position) -> int:
        return self.__body.collidepoint(mouse_position) or self.__bottom_border.collidepoint(mouse_position)

    def __mouse_pressed(self) -> bool:
        return pygame.mouse.get_pressed()[0] == 1


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

if __name__ == '__main__':
    pass
