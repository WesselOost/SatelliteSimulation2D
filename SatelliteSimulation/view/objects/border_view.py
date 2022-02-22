# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pygame
from SatelliteSimulation.view.resources import Color


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class BorderView:
    """
    A Border with black background and light grey outline
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, x: float, y: float, width: float, height: float, margin: float, padding: float, line_width: int):
        self.__border: pygame.Rect = pygame.Rect(x + margin, y + margin, width, height)
        self.__padding: float = padding
        self.__margin: float = margin
        self.__padded_border: pygame.Rect = pygame.Rect(self.__border.x + padding,
                                                        self.__border.y + padding,
                                                        self.__border.width - (padding * 2),
                                                        self.__border.height - (padding * 2))
        self.__line_width: int = line_width

        self.__show_padding: bool = False


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def padding(self) -> float:
        return self.__padding


    @property
    def margin(self) -> float:
        return self.__margin

    @property
    def line_width(self) -> int:
        return self.__line_width


    def get_border_rectangle(self) -> pygame.Rect:
        return self.__border


    def show_padding(self, show_padding: bool):
        self.__show_padding = show_padding


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, Color.BLACK, self.__border)
        pygame.draw.rect(surface, Color.LIGHT_GREY, self.__border, self.__line_width)
        if self.__show_padding:
            pygame.draw.rect(surface, Color.RED, self.__padded_border, 1)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #


#  SECTION: Function definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #

