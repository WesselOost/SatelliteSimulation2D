# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from view.resources import Color


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class SatelliteObservanceBorderView:
    """
    A circle outline object.
    """
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    DEFAULT_LINE_THICKNESS = 4


    def __init__(self, color: Color, position: tuple, radius: float, line_thickness: int):
        self.__color: Color = color
        self.__position: tuple = position
        self.__radius: float = radius
        self.__line_thickness: int = line_thickness


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def color(self) -> Color:
        return self.__color


    @property
    def position(self) -> tuple:
        return self.__position


    @property
    def radius(self) -> float:
        return self.__radius


    @property
    def line_thickness(self) -> int:
        return self.__line_thickness
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #
