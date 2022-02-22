
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
    """
    container for all the buttons.
    """

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
                self.__buttons[name] = ToggleButton(0, 0, width, font_size, name, on_clicked_handler, data.is_selected)
            else:
                button = Button(0, 0, width, font_size, name, on_clicked_handler)
                self.__buttons[name] = button
                if data.button_state == ButtonState.DISABLED:
                    button.disable()

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
        # set selected state of the toggle buttons
        [toggle_button_data.set_is_selected(self.__buttons[toggle_button_data.button_name].is_selected)
         for toggle_button_data in self.__button_data if toggle_button_data.button_type == ButtonType.TOGGLE_BUTTON]

        [button_data.set_button_state(self.__buttons[button_data.button_name].state)
         for button_data in self.__button_data if button_data.button_type == ButtonType.BUTTON]

        [print(self.__buttons[button_data.button_name].state)
         for button_data in self.__button_data if button_data.button_type == ButtonType.BUTTON]

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
            self.__buttons[button_name].handle_state_changed()


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

