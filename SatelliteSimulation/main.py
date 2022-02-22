#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tom Brandherm & Wessel Oostrum
# @Python  : 3.6.8
# @Version : 1.0.0
"""
Main module for the satellite simulation. Execute this to start the program.
"""

# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #
import logging
import os
import pandas as pd
from presenter.presenter import Presenter




# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #
ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Function definitions
# =========================================================================== #


def read_excel_file(file: str) -> pd.DataFrame:
    return pd.read_excel(file, header=0, engine='openpyxl', index_col=0)

def main():
    config_file_path: str = os.path.join(ABSOLUTE_PATH, "config.xlsx")
    config_data: pd.DataFrame = read_excel_file(file=config_file_path)
    Presenter(config_data=config_data)


# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    # level = logging.INFO
    level = logging.DEBUG
    # level = logging.ERROR
    format = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=format)
    main()

