# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import pygame


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class NavigationHandler:
    """
    Handles new keyboard arrow click events
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self):
        self.pressed_left: bool = False
        self.pressed_up: bool = False
        self.pressed_right: bool = False
        self.pressed_down: bool = False
        pass
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #
    def get_button_states(self):
        return self.pressed_left, self.pressed_up, self.pressed_right, self.pressed_down
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def should_navigate(self)-> bool:
        return self.pressed_left or self.pressed_up or self.pressed_right or self.pressed_down

    def handle_key_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.pressed_left = True
            elif event.key == pygame.K_RIGHT:
                self.pressed_right = True
            elif event.key == pygame.K_UP:
                self.pressed_up = True
            elif event.key == pygame.K_DOWN:
                self.pressed_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.pressed_left = False
            elif event.key == pygame.K_RIGHT:
                self.pressed_right = False
            elif event.key == pygame.K_UP:
                self.pressed_up = False
            elif event.key == pygame.K_DOWN:
                self.pressed_down = False
    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


