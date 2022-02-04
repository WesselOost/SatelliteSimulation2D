# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-10-28 13:51:47
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Link    : link
# @Version : 0.0.1
"""
Class Description
"""


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


class AutoDisturbances:

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
        logging.info('start thread')
        if not self.__thread.is_alive():
            self.__stop_thread = False
            self.__thread = threading.Thread(target=self.__run, args=(lambda: self.__stop_thread,))
            self.__thread.daemon = True
            self.__thread.start()


    def stop(self):
        if self.__thread.is_alive():
            self.__stop_thread = True
            logging.info('thread stopped')

    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Private Methods
    # ----------------------------------------------------------------------- #

    def __run(self, stop):
        while True:
            self.__controller.on_disturbance_clicked(self.__get_random_disturbance().value)
            time.sleep(random.uniform(0.1, 1.0))

            if stop():
                break

    # =========================================================================== #
    #  SECTION: Function definitions
    # =========================================================================== #
    def __get_random_disturbance(self) -> DisturbanceType:
        return choice(self.__disturbanceTypes, 1, p=[0.70, 0.10, 0.10, 0.10])[0]

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #


if __name__ == '__main__':
    auto = AutoDisturbances()
    auto.start()
    time.sleep(10)
    auto.stop()
