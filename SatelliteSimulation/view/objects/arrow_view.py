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


class ArrowView:
    """
    Data container for drawing an arrow
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, start_of_line: tuple, end_of_line: tuple, arrow_head: list, line_thickness: int):
        self.__start_of_line: tuple = start_of_line
        self.__end_of_line: tuple = end_of_line
        self.__arrow_head: list = arrow_head
        self.__line_thickness: int = line_thickness


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    @property
    def start_of_line(self) -> tuple:
        return self.__start_of_line


    @property
    def end_of_line(self) -> tuple:
        return self.__end_of_line


    @property
    def arrow_head(self) -> list:
        return self.__arrow_head


    @property
    def line_thickness(self) -> int:
        return self.__line_thickness


    @property
    def color(self) -> Color:
        return Color.RED

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


