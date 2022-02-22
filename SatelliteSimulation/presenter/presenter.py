# =========================================================================== #
#  SECTION: Imports
# =========================================================================== #

import os
import random
import sys
import pandas as pd

sys.dont_write_bytecode = True
sys.path.append(os.getcwd())

from presenter.auto_disturbances import AutoDisturbancesHandler
from model.arrow import Arrow
from model.basic_math.vector import multiply, Vector, add
from model.satellite.satellite import Satellite
from view.objects.arrow_view import ArrowView
from view.objects.button.button_control_panel_view import ButtonControlPanelView
from view.objects.button.button_data import ButtonData, ToggleButtonData
from view.objects.button.pygame_button import ButtonType
from view.objects.satellite_observance_border_view import SatelliteObservanceBorderView
from view.objects.satellite_view import SatelliteView
from view.resources import Color
from model.disturbance.disturbance_type import DisturbanceType
from model.model import Space
from model.border import Border
from view.view import GUI


# =========================================================================== #
#  SECTION: Global definitions
# =========================================================================== #

# =========================================================================== #
#  SECTION: Class definitions
# =========================================================================== #


class Presenter:
    """
    This class connects the model (Space) and the view layer (GUI). It initiates their data.
    It requests the model layer to update,
    retrieves data from the model,
    converts them to ui objects,
    requests the view layer to update the UI
    and receive user events from the view layer.
    """


    # ----------------------------------------------------------------------- #
    #  SUBSECTION: Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, debug_mode=False, config_data: pd.DataFrame=None):
        self.__debug_mode: bool = debug_mode
        self.__config_data: pd.DataFrame = config_data
        self.__border: Border = Border(x=0, y=0, width=1920, height=1080, padding=30)

        self.space = Space(satellite_amount=random.randint(15, 20), 
                           border=self.__border,
                           config_data=self.__config_data)

        button_data: list = [ButtonData(button_name=disturbance_type.value,
                                        on_click_handler=self.on_disturbance_clicked
                                        ) for disturbance_type in DisturbanceType]

        # add auto disturbance toggle button
        button_data.append(ToggleButtonData(button_name="AUTOMATIC RANDOM DISTURBANCES",
                                            on_click_handler=self.on_auto_disturbance_clicked,
                                            is_selected=False
                                            ))

        self.gui = GUI(controller=self,
                       border_width=self.__border.width(),
                       border_height=self.__border.height(),
                       border_padding=self.__border.padding(),
                       button_data=button_data)

        self.__auto_disturbance_thread: AutoDisturbancesHandler = AutoDisturbancesHandler(self)

        self.__run = True
        self.start_simulation_loop()

        # ----------------------------------------------------------------------- #
        #  SUBSECTION: Getter/Setter
        # ----------------------------------------------------------------------- #

        # ----------------------------------------------------------------------- #
        #  SUBSECTION: Public Methods
        # ----------------------------------------------------------------------- #


    def start_simulation_loop(self):
        while self.__run:
            self.set_delta_time(self.gui.calculate_delta_time())
            self.gui.handle_events()
            self.gui.calculate_button_states_and_handle_click_events()
            self.gui.handle_user_navigation()
            self.next_frame()
        self.gui.quit()


    def quit(self):
        self.__run = False


    def on_disturbance_clicked(self, disturbance_type_name: str):
        self.space.create_disturbance(DisturbanceType(disturbance_type_name))


    def on_auto_disturbance_clicked(self, is_selected: bool):
        control_panel_view: ButtonControlPanelView = self.gui.button_control_panel_view
        disturbance_types = [disturbance_type.value for disturbance_type in DisturbanceType]
        if is_selected:
            self.__auto_disturbance_thread.start()
            control_panel_view.disable(disturbance_types)
        else:
            self.__auto_disturbance_thread.stop()
            control_panel_view.enable(disturbance_types)


    def steer_satellite(self, pressed_left: bool, pressed_up: bool, pressed_right: bool, pressed_down: bool):
        if self.__debug_mode:
            self.space.manually_steer_satellite(pressed_left, pressed_up, pressed_right, pressed_down)


    def set_delta_time(self, delta_time: float):
        self.space.set_delta_time(delta_time)


    def next_frame(self):
        scale_factor: float = self.gui.get_satellite_border_scale()
        self.space.avoid_possible_future_collisions()
        self.space.move_satellites()
        satellites: list = self.space.get_satellites()
        self.space.update_satellite_observance()
        self.space.check_and_handle_collisions()

        offset: float = self.gui.get_satellite_border_margin() + self.gui.get_satellite_border_padding()
        arrows: list = [arrow_to_arrow_view(arrow, scale_factor, offset) for arrow in self.space.get_velocity_arrows()]
        satellite_views: list = [satellite_to_satellite_view(satellite, scale_factor, offset) for satellite in
                                 satellites]
        satellite_borders: list = [satellite_to_observance_border_view(satellite, scale_factor, offset)
                                   for satellite in satellites if not satellite.is_crashed()]

        self.gui.update(satellite_views, arrows, satellite_borders)


    def get_satellite_border(self) -> tuple:
        border = self.space.get_border()
        return border.x(), border.y(), border.width(), border.height(), border.padding()

        # ----------------------------------------------------------------------- #
        #  SUBSECTION: Private Methods
        # ----------------------------------------------------------------------- #

        # =========================================================================== #
        #  SECTION: Function definitions
        # =========================================================================== #


def arrow_to_arrow_view(arrow: Arrow, scale_factor: float, offset: float) -> ArrowView:
    arrow_offset: Vector = Vector(offset, offset)
    return ArrowView(start_of_line=scale_and_add_offset(arrow.start_of_line(), scale_factor, arrow_offset),
                     end_of_line=scale_and_add_offset(arrow.end_of_line(), scale_factor, arrow_offset),
                     arrow_head=[scale_and_add_offset(arrow.head_left(), scale_factor, arrow_offset),
                                 scale_and_add_offset(arrow.head_right(), scale_factor, arrow_offset),
                                 scale_and_add_offset(arrow.head_tip(), scale_factor, arrow_offset)],
                     line_thickness=max(1, int(arrow.line_thickness() * scale_factor)))


def scale_and_add_offset(vector: Vector, scale_factor: float, offset: Vector) -> tuple:
    return add(vector1=multiply(vector, scale_factor), vector2=offset).get_as_tuple()


def satellite_to_satellite_view(satellite: Satellite, scale_factor: float, offset: float) -> SatelliteView:
    x = (scale_factor * satellite.position.x()) + offset
    y = (scale_factor * satellite.position.y()) + offset
    return SatelliteView(x,
                         y,
                         int(scale_factor * satellite.size()),
                         satellite.is_crashed(),
                         satellite.get_type())


def satellite_to_observance_border_view(satellite: Satellite, scale_factor: float,
                                        offset: float) -> SatelliteObservanceBorderView:
    color = Color.ORANGE if satellite.observed_satellites() else Color.GREY

    if satellite.possible_collisions():
        color = Color.RED

    line_thickness: int = max(1, int(SatelliteObservanceBorderView.DEFAULT_LINE_THICKNESS * scale_factor))
    position = add(multiply(satellite.center(), scale_factor), Vector(offset, offset)).get_as_tuple()

    return SatelliteObservanceBorderView(color=color,
                                         position=position,
                                         radius=(satellite.radius() + satellite.observance_radius()) * scale_factor,
                                         line_thickness=line_thickness)

    # =========================================================================== #
    #  SECTION: Main Body
    # =========================================================================== #
