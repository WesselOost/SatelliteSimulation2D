# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from enum import Enum
from view.resources.Color import *
import pygame


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class ButtonState(Enum):
    RELEASED = "released"
    HOVERED = "hovered"
    PRESSED = "pressed"
    DISABLED = "disabled"


class ButtonType(Enum):
    BUTTON = "button"
    TOGGLE_BUTTON = "toggle_button"


class Button:
    """
    Button module for pygame.
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, y: float, width: float, font_size: float, button_text: str, on_clicked_handler):
        self._on_clicked_handler = on_clicked_handler
        self.__state: ButtonState = ButtonState.RELEASED
        self._new_click_event: bool = False
        self.__reference_x: float = x
        self.__reference_y: float = y
        self.__reference_width: float = width
        self.x: float = x
        self.y: float = y
        self.__font_size_reference: float = font_size
        self.__font_size: float = font_size
        self._hover_color: tuple = GREEN
        self._released_color: tuple = LIGHT_BLUE

        self.__init_button(button_text, font_size, width)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def set_position(self, new_x: float, new_y: float):
        self.x = new_x
        self.y = new_y
        self.__body.x = new_x
        self.__body.y = new_y
        self.__bottom_border.x = new_x
        self.__bottom_border.y = new_y + self.__body_height


    def get_width(self) -> float:
        return self.__width


    def get_height(self) -> int:
        return self.__body_height + self.__bottom_border_height


    def get_text(self) -> str:
        return self.__button_text


    @property
    def state(self) -> ButtonState:
        return self.__state


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    def draw(self, surface: pygame.Surface):
        self.__draw_bottom_border(surface)
        self.__draw_body(surface)
        self.__draw_text(surface)


    def disable(self):
        self.__set_state(ButtonState.DISABLED, int(self.y), GREY)
        self._body_color = MEDIUM_GREY


    def enable(self):
        self.__set_state(ButtonState.RELEASED, int(self.y), LIGHT_BLUE)
        self._body_color = BLUE


    def handle_state_changed(self):
        if self.__state is not ButtonState.DISABLED:
            mouse_position = pygame.mouse.get_pos()
            self._new_click_event = False
            if self.__pressed_and_state_is_hovered(mouse_position):
                self.__set_state(ButtonState.PRESSED, int(self.__body.y + self.__bottom_border.height), TRANSPARENT)
                self._new_click_event = True
            elif self.__hovered_and_state_changed(mouse_position):
                self.__set_state(ButtonState.HOVERED, int(self.y), self._hover_color)
            elif self.__released_and_state_changed(mouse_position):
                self.__set_state(ButtonState.RELEASED, int(self.y), self._released_color)


    def new_click_event(self) -> bool:
        return self._new_click_event


    def activate_click_handler(self):
        self._on_clicked_handler(self.__button_text)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __init_button(self, button_text: str, font_size: float, width: float):
        # init button text
        self.__font = pygame.font.SysFont("Verdana", int(font_size))
        self.__anti_alias = True
        self.__button_text = button_text
        self.__text_surface = self.__font.render(self.__button_text, self.__anti_alias, LIGHT_GREY)

        offset = self.__text_surface.get_height()
        self.__width = width
        self.__text_offset_x = (self.__width - self.__text_surface.get_width()) // 2
        self.__text_offset_y = offset // 2

        # init button body
        self.__body_height = self.__text_surface.get_height() + offset
        self._body_color = BLUE
        self.__body = pygame.Rect(self.x, self.y, self.__width, self.__body_height)

        # init button border
        self.__bottom_border_height = self.__body_height / 8
        self._bottom_border_color = LIGHT_BLUE
        self.__bottom_border = pygame.Rect(self.x,
                                           self.__body_height + self.y,
                                           self.__width,
                                           self.__bottom_border_height)


    def __draw_bottom_border(self, surface):
        pygame.draw.rect(surface, self._bottom_border_color, self.__bottom_border)


    def __draw_body(self, surface):
        corner_arch = int(self.__body_height // 4)
        pygame.draw.rect(surface, self._body_color, self.__body, 0, 0, corner_arch, corner_arch)


    def __draw_text(self, surface):
        surface.blit(self.__text_surface, (self.x + self.__text_offset_x, self.__body.y + self.__text_offset_y))


    def __set_state(self, state: ButtonState, body_y: int, border_color: tuple):
        self.__state = state
        self.__body.y = body_y
        self._bottom_border_color = border_color


    def __pressed_and_state_is_hovered(self, mouse_position) -> bool:
        return self.__mouse_collide_with_button(mouse_position) and \
               self.__mouse_pressed() and \
               self.__state == ButtonState.HOVERED


    def __hovered_and_state_changed(self, mouse_position) -> bool:
        return self.__mouse_collide_with_button(mouse_position) and \
               not self.__mouse_pressed() and \
               self.__state != ButtonState.HOVERED


    def __released_and_state_changed(self, mouse_position) -> bool:
        return not self.__mouse_collide_with_button(mouse_position) and \
               not self.__mouse_pressed() \
               and self.__state != ButtonState.RELEASED


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
class ToggleButton(Button):
    """
    button that can be on or off.
    """

    def __init__(self, x: float, y: float, width: float, font_size: float, button_text: str, on_clicked_handler, is_selected: bool):
        super().__init__(x, y, width, font_size, button_text, on_clicked_handler)
        self.__is_selected: bool = is_selected
        self.__selected_on_changed()


    @property
    def is_selected(self):
        return self.__is_selected


    def activate_click_handler(self):
        self.__is_selected = not self.__is_selected
        self._on_clicked_handler(self.__is_selected)
        self.__selected_on_changed()


    def __selected_on_changed(self):
        if self.__is_selected:
            self.__set_colors(body_color=DARK_GREEN, bottom_border_color=GREEN, hover_color=LIGHT_BLUE)
        else:
            self.__set_colors(body_color=BLUE, bottom_border_color=LIGHT_BLUE, hover_color=GREEN)


    def __set_colors(self, body_color: tuple, bottom_border_color: tuple, hover_color: tuple):
        self._body_color: tuple = body_color
        self._bottom_border_color: tuple = bottom_border_color
        self._hover_color: tuple = hover_color
        self._released_color: tuple = bottom_border_color


