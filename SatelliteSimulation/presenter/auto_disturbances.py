# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import logging
import random
import threading
import time
from numpy.random import choice
from SatelliteSimulation.model.disturbance.disturbance_type import DisturbanceType


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class AutoDisturbancesHandler:
    """
    A Thread class which creates at random intervals a random Disturbance type.
    The DisturbanceTypes are weighted.
    """

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #
    def __init__(self, controller):
        self.__controller = controller
        self.__stop_thread: bool = False
        self.__thread: threading.Thread = threading.Thread()
        self.__disturbanceTypes: list = list(DisturbanceType)

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Getter/Setter
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Public Methods
    # ----------------------------------------------------------------------- #
    def start(self):
        if not self.__thread.is_alive():
            self.__stop_thread = False
            self.__thread = threading.Thread(target=self.__run, args=(lambda: self.__stop_thread,))
            self.__thread.daemon = True
            self.__thread.start()


    def stop(self):
        if self.__thread.is_alive():
            self.__stop_thread = True

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __run(self, stop):
        while True:
            self.__controller.on_disturbance_clicked(self.__get_random_disturbance().value)
            time.sleep(random.uniform(0.3, 1.3))

            if stop():
                break

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #
    def __get_random_disturbance(self) -> DisturbanceType:
        weights_of_the_disturbance_type = [0.70, 0.10, 0.10, 0.10]
        return choice(self.__disturbanceTypes, 1, p=weights_of_the_disturbance_type)[0]

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


