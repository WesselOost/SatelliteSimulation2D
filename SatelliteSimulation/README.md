# Satellite Simulation in 2D

## Introduction

This program is a 2D simulation of satellites in the earth orbit. A small cutout from the space is shown and all satellites have the same initial velocity.
The used navigation alogrithm should prevent the satellites from collisions. A position change of satellites is influenced by:

* a malefunction
* a gravitational disturbance
* a electromagnetic disturbance
* a dirsturbance based on solar radiation pressure

## Table of Contents

1. [Introduction](#Introdurction)[How to use](#Howtouse)
2. 1. [Setup](#Setup)
   2. [Usage](#Usage)
3. [Contributing](#Contributing)
4. [Links](#Links)

## How to use

### Setup

* The tool is written in Python and the version **3.6.8** is used.
* **Installation of used libaries**
  The used libaries (that are not installed by default) are listed in the **`requirements.txt`** file.
  To install them use the command: *pip install -r `requirements.txt`*
* In the ***`config.xlsx`*** *file can the `obervance-radius`* (radius in which a satellite is oberving other satellites) of the satellites be adjusted.
  Values are valid in the range **[0, 300].**

### Usage

After the setup ![test image](SatelliteSimulation\Assets\asteroid1.png)

```python
# =========================================================================== #
#  SECTION: Main Body
# =========================================================================== #
if __name__ == '__main__':
    main(analyse_pdf=False)
```

The `analyse_pdf` parameter is per default on True.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Links

Helpfull links:

* [link](https://letmegooglethat.com/)
