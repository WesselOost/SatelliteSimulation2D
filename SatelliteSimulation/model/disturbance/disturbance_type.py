# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
from enum import Enum


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class DisturbanceType(Enum):
    """
    Disturbance types that can affect satellites in space
    """
    MALFUNCTION = "MALFUNCTION"
    MAGNETIC = "ELECTROMAGNETIC DISTURBANCE"
    SOLAR_RADIATION = "SOLAR RADIATION DISTURBANCE"
    GRAVITATIONAL = "GRAVITY GRADIENT DISTURBANCE"

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

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
