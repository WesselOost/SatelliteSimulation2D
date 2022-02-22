# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
import pygame

from SatelliteSimulation.view.objects.border_view import BorderView
from SatelliteSimulation.view.objects.button.button_control_panel_view import ButtonControlPanelView
from SatelliteSimulation.view.objects.button.button_data import ButtonData
from SatelliteSimulation.view.objects.earth_view import EarthView

BORDER_PERCENTAGE = 0.75
MARGIN_PERCENTAGE = 0.01
MINI_BORDER_SCALE = 0.04
FONT_SIZE = 24
DEFAULT_BUTTON_OFFSET = 50


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class ViewStore:
    """
    Creates the layout for the Border, ButtonControls and earth.
    It defines the initial size of the view objects based on the input parameters.
    Reference to the initial size is saved inorder to scale the view objects.
    """


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, width: float, height: float, padding: float, button_data: list):
        # create border view
        border_view_width: float = width * BORDER_PERCENTAGE
        border_view_height: float = height * BORDER_PERCENTAGE
        border_padding: float = padding * BORDER_PERCENTAGE
        margin: float = width * MARGIN_PERCENTAGE
        self.__border_reference: BorderView = BorderView(0, 0, border_view_width, border_view_height, margin,
                                                         border_padding,
                                                         line_width=max(1, int(height * 0.004)))

        # create button control
        border_as_rectangle: pygame.Rect = self.__border_reference.get_border_rectangle()
        left_over_width: float = width - border_as_rectangle.width - border_as_rectangle.x
        button_width: float = left_over_width - (margin * 5)
        button_x: float = (width - left_over_width) + margin * 3
        button_y: float = border_as_rectangle.y + margin
        self.__button_control_panel_reference: ButtonControlPanelView = ButtonControlPanelView(button_x,
                                                                                               button_y,
                                                                                               button_width,
                                                                                               height_padding=margin,
                                                                                               font_size=button_width * 0.05,
                                                                                               button_data=button_data)

        # create earth
        border_center_x: float = border_as_rectangle.center[0]
        left_over_height: float = height - border_as_rectangle.height - border_as_rectangle.y
        earth_size: float = left_over_height
        dotted_circle_padding: float = (left_over_height - (earth_size / 2)) * .5
        self.__earth_reference: EarthView = EarthView(border_center_x, height, earth_size, dotted_circle_padding)

        # create mini border
        mini_border_width = border_as_rectangle.width * MINI_BORDER_SCALE
        mini_border_height = border_as_rectangle.height * MINI_BORDER_SCALE
        mini_border_x = border_center_x - mini_border_width // 2
        mini_border_y = self.__earth_reference.get_dotted_circle_position()[1] - mini_border_height // 2
        self.__mini_border_reference: BorderView = BorderView(mini_border_x,
                                                              mini_border_y,
                                                              mini_border_width,
                                                              mini_border_height,
                                                              margin=0,
                                                              padding=0,
                                                              line_width=1)

        self.__border = self.__scale_border_view(self.__border_reference, 1)
        self.__button_control_panel = self.__scale_button_control_panel(1, self.__button_control_panel_reference.button_data)
        self.__earth = self.__scale_earth(1)
        self.__mini_border = self.__scale_border_view(self.__mini_border_reference, 1)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def get_satellite_border_percentage(self) -> float:
        return BORDER_PERCENTAGE


    @property
    def border(self) -> BorderView:
        return self.__border

    @property
    def mini_border(self)-> BorderView:
        return self.__mini_border

    @property
    def earth(self)-> EarthView:
        return self.__earth

    @property
    def button_control_panel(self) -> ButtonControlPanelView:
        return self.__button_control_panel

    def scale_views(self, scale_factor: float):
        self.__earth = self.__scale_earth(scale_factor)
        self.__button_control_panel = self.__scale_button_control_panel(scale_factor,  self.__button_control_panel.button_data)
        self.__border = self.__scale_border_view(self.__border_reference, scale_factor)
        self.__mini_border = self.__scale_border_view(self.__mini_border_reference, scale_factor)


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __scale_earth(self, scale_factor:float):
        earth: EarthView = self.__earth_reference
        center_x: float = earth.center_x * scale_factor
        surface_height: float = earth.surface_height * scale_factor
        earth_size: float = earth.earth_size * scale_factor
        dotted_circle_padding: float = earth.dotted_circle_padding * scale_factor
        return EarthView(center_x, surface_height, earth_size, dotted_circle_padding)


    def __scale_button_control_panel(self, scale_factor:float, button_data: list):
        button_control_panel: ButtonControlPanelView = self.__button_control_panel_reference
        x: float = button_control_panel.x * scale_factor
        y: float = button_control_panel.y * scale_factor
        width: float = button_control_panel.width * scale_factor
        padding: float = button_control_panel.height_padding * scale_factor
        font_size: float = button_control_panel.font * scale_factor
        return ButtonControlPanelView(x, y, width, padding, font_size, button_data)


    def __scale_border_view(self, border: BorderView, scale_factor:float):
        border_as_rectangle: pygame.Rect = border.get_border_rectangle()
        x: float = border_as_rectangle.x * scale_factor
        y: float = border_as_rectangle.y * scale_factor
        width: float = border_as_rectangle.width * scale_factor
        height: float = border_as_rectangle.height * scale_factor
        margin: float = border.margin * scale_factor
        padding: float = border.padding * scale_factor
        line_width: int = max(1, int(border.line_width * scale_factor))
        return BorderView(x, y, width, height, margin, padding, line_width)

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #
