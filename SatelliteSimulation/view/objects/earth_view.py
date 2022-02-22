# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pygame

from SatelliteSimulation.view.resources.images import Images

# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #


# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #
class EarthView:
    """
    An earth Icon that rotates with a dotted outline around it
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, center_x: float, surface_height: float, earth_size: float, dotted_circle_padding):
        images = Images()
        self.__earth_img: pygame.Surface = images.get_earth()
        self.__dotted_circle: pygame.Surface = images.get_dotted_circle()


        self.__earth_img = pygame.transform.scale(self.__earth_img, (earth_size, earth_size))
        self.__center_x = center_x
        self.__dotted_circle_padding = dotted_circle_padding
        self.__earth_img_angle = 0

        self.__earth_size = earth_size
        self.__surface_height = surface_height

        self.__dotted_circle_padding = dotted_circle_padding
        dotted_circle_size: float = earth_size + dotted_circle_padding
        dotted_circle_x: float = center_x - (dotted_circle_size // 2)
        dotted_circle_y: float = surface_height - (dotted_circle_size // 2)
        self.__dotted_circle_position: tuple = (dotted_circle_x, dotted_circle_y)
        self.__dotted_circle: pygame.Surface = pygame.transform.scale(self.__dotted_circle,
                                                                      (dotted_circle_size, dotted_circle_size))


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    @property
    def center_x(self) -> float:
        return self.__center_x
    @property
    def surface_height(self) -> float:
        return self.__surface_height
    @property
    def earth_size(self) -> float:
        return self.__earth_size
    @property
    def dotted_circle_padding(self) -> float:
        return self.__dotted_circle_padding

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def draw(self, surface: pygame.Surface):
        surface.blit(self.__dotted_circle, self.__dotted_circle_position)
        self.__rotate_and_draw_earth(surface)


    def get_dotted_circle_position(self) -> tuple:
        return self.__dotted_circle_position[0], self.__dotted_circle_position[1]


    def get_dotted_circle_width(self) -> int:
        return self.__dotted_circle.get_width()


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #


    def __rotate_and_draw_earth(self, surface: pygame.Surface):
        self.__earth_img_angle -= 0.2
        earth_img_rotated = pygame.transform.rotozoom(self.__earth_img, self.__earth_img_angle, 1)
        image_position = (self.__center_x - earth_img_rotated.get_width() // 2), \
                         surface.get_height() - earth_img_rotated.get_height() // 2

        surface.blit(earth_img_rotated, image_position)


# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
