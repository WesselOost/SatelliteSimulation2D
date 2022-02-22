# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from view.objects.button.pygame_button import ButtonType, ButtonState


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class ButtonData:
    """
    Data container for button name, button type and the function that should be called when the button is clicked.
    """


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, button_name: str, on_click_handler, button_state=ButtonState.RELEASED):
        self.__button_name: str = button_name
        self.__on_clicked_handler = on_click_handler
        self.__button_state = button_state


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def button_name(self) -> str:
        return self.__button_name


    @property
    def button_type(self) -> ButtonType:
        return ButtonType.BUTTON


    @property
    def button_state(self) -> ButtonState:
        return self.__button_state



    def set_button_state(self, button_state: ButtonState):
        self.__button_state = button_state


    @property
    def on_clicked_handler(self):
        return self.__on_clicked_handler
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #


class ToggleButtonData(ButtonData):

    def __init__(self, button_name: str, on_click_handler, is_selected):
        super().__init__(button_name, on_click_handler)
        self.__is_selected = is_selected


    @property
    def is_selected(self):
        return self.__is_selected


    @property
    def button_type(self) -> ButtonType:
        return ButtonType.TOGGLE_BUTTON

    def set_is_selected(self, is_selected):
        self.__is_selected = is_selected

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
