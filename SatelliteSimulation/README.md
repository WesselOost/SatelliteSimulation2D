# Satellite Simulation in 2D
![test image](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/demo/demo.gif?raw=true)

## Introduction

This program is a 2D simulation of satellites in the earth orbit. A small cutout from the space is shown and all satellites have the same initial velocity.
The used navigation alogrithm should prevent the satellites from collisions. A position change of satellites is influenced by:

* a malefunction &rarr; one randome satellite is unbale to navigate and changes its position randomly
* a gravitational disturbance &rarr; the satelites are disturbed randomly in dependency of their mass in positive or negative y-direction
* a electromagnetic disturbance &rarr; the satelites are disturbed randomly in dependency of their charge (&#126;mass) in any direction
* a dirsturbance based on solar radiation pressure &rarr; the satelites are disturbed randomly in dependency of their surface in any direction

The simulation contains the following satellites objects with the normal and destroyed state:

|name      | normal state | destroyed state
----------|:--------------:|:----------------:
|SatelliteA| ![SatelliteA](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/satellite1.png?raw=true)| ![test image](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/satellite1_crashed.png?raw=true)|
|SatelliteB| ![SatelliteB](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/satellite2.png?raw=true)| ![test image](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/satellite2_crashed.png?raw=true)|
|SatelliteC| ![SatelliteC](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/satellite3.png?raw=true)| ![test image](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/satellite3_crashed.png?raw=true)|
|SatelliteD| ![SatelliteD](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/satellite4.png?raw=true)| ![test image](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/satellite4_crashed.png?raw=true)|
|SpaceJunk| ![SpaceJunk](https://github.com/WesselOost/studienProjekt2/blob/2022-02-22_refactoring/SatelliteSimulation/Assets/asteroid1.png?raw=true)| - |
 
 If a satellite collides is changes from the ***normal*** into the ***destroyed state***. A destroyed satellite becomes like the SpaceJunk object unable to navigate.

## How to use

### Setup

* The tool is written in Python and the version **3.6.8** is used.
* **Installation of used libaries**
  The used libaries (that are not installed by default) are listed in the **`requirements.txt`** file.
  To install them use the command: 
  
  ```console
  pip install -r requirements.txt
  ```
  
* In the ***`config.xlsx`*** *file can the `obervance-radius`* (radius in which a satellite is oberving other satellites) of the satellites be adjusted.
  Values are valid in the range **[0, 300].**

### Usage

After the setup is complete the ***`main.py`*** file can be executed from the ***`SatelliteSimulation/`*** directory with the command:
```console
  python main.py
  ```
The `main()` function reads in the config data from the config file and creates a `Presenter` objects. The used ***MVP*** architecture allows this object to control the `View` and the `model` layer of the program.
```python
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
    level = logging.DEBUg
    format = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=format)
    main()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Links

Helpfull links:

* [link](https://letmegooglethat.com/)
