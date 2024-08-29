from academy.task_collection import Task
from pybpodapi.protocol import Bpod
from academy.utils import utils
from user import settings
import random
import numpy as np
from scipy.signal import firwin, lfilter


class LED_test(Task):

    def __init__(self):
        super().__init__()

        self.info = """
        ########   TASK INFO   ########
        Testing
        """

    def init_variables(self):
        self.trials_max = 10

        # pumps
        if settings.BOX_NAME == 9:
            self.valve_l_time = utils.water_calibration.read_last_value('port', 2).pulse_duration
            self.valve_l_reward = utils.water_calibration.read_last_value('port', 2).water
            self.valve_r_time = utils.water_calibration.read_last_value('port', 5).pulse_duration
            self.valve_r_reward = utils.water_calibration.read_last_value('port', 5).water
        elif settings.BOX_NAME == 12:
            self.valve_l_time = utils.water_calibration.read_last_value('port', 7).pulse_duration
            self.valve_l_reward = utils.water_calibration.read_last_value('port', 7).water
            self.valve_r_time = utils.water_calibration.read_last_value('port', 1).pulse_duration
            self.valve_r_reward = utils.water_calibration.read_last_value('port', 1).water


        self.led_intensity = 255

    def configure_gui(self):  # Variables that appear in the GUI
        self.gui_input = ['trials_max']

    def main_loop(self):
        if settings.BOX_NAME == 9:
            portLeftIn = Bpod.Events.Port2In
            portCenterIn = Bpod.Events.Port3In
            portRightIn = Bpod.Events.Port5In

            portLeftOut = Bpod.Events.Port2Out
            portCenterOut = Bpod.Events.Port3Out
            portRightOut = Bpod.Events.Port5Out

            ledLeft = (Bpod.OutputChannels.PWM2, self.led_intensity)
            ledCenter = (Bpod.OutputChannels.PWM3, self.led_intensity)
            ledRight = (Bpod.OutputChannels.PWM5, self.led_intensity)

            valveLeft = (Bpod.OutputChannels.Valve, 2)
            valveRight = (Bpod.OutputChannels.Valve, 5)

        elif settings.BOX_NAME == 12:
            portLeftIn = Bpod.Events.Port7In
            portCenterIn = Bpod.Events.Port4In
            portRightIn = Bpod.Events.Port1In
            portLeftOut = Bpod.Events.Port7Out
            portCenterOut = Bpod.Events.Port4Out
            portRightOut = Bpod.Events.Port1Out
            ledLeft = (Bpod.OutputChannels.PWM7, self.led_intensity)
            ledCenter = (Bpod.OutputChannels.PWM4, self.led_intensity)
            ledRight = (Bpod.OutputChannels.PWM1, self.led_intensity)
            valveLeft = (Bpod.OutputChannels.Valve, 7)
            valveRight = (Bpod.OutputChannels.Valve, 1)
    

        self.sma.add_state(
            state_name='waiting',
            state_timer=10,
            state_change_conditions={Bpod.Events.Tup: 'exit', portLeftIn: 'left', portCenterIn:'center', portRightIn: 'right'},
            output_actions=[]
        )

        self.sma.add_state(
            state_name='left',
            state_timer=0,
            state_change_conditions={portLeftOut: 'waiting'},
            output_actions=[ledLeft]
        )

        self.sma.add_state(
            state_name='center',
            state_timer=0,
            state_change_conditions={portCenterOut: 'waiting'},
            output_actions=[ledCenter]
        )

        self.sma.add_state(
            state_name='right',
            state_timer=0,
            state_change_conditions={portRightOut: 'waiting'},
            output_actions=[ledRight]
        )









