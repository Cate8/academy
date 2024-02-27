from academy.task_collection import Task
from pybpodapi.protocol import Bpod
from academy.utils import utils
from user import settings
import random
import numpy as np
from scipy.signal import firwin, lfilter


class S1(Task):

    def __init__(self):
        super().__init__()

        self.info = """
        ########   TASK INFO   ########
        teack mice to approach lickports

        Starts with reward sound ON + water port LED ON + automatic delivery of water.
        Sound and LED stay on until poke or timeup. Global lights always ON.

        ########   PORTS INFO   ########
        Port 1 - Right port
        Port 3 - Central port
        Port 5 - Left port
        """
        

    def init_variables(self):
        # general
        self.stage = 0
        self.substage = 0
        self.trials_max = 60
        self.side = random.choice(["left", "right"])
        self.trials_with_same_side = 20
        self.trial_count = 0
        self.same_side_count = 0

        # pumps
        self.valve_r_time = utils.water_calibration.read_last_value('port', 2).pulse_duration
        self.valve_r_reward = utils.water_calibration.read_last_value('port', 2).water
        self.valve_l_time = utils.water_calibration.read_last_value('port', 5).pulse_duration
        self.valve_l_reward = utils.water_calibration.read_last_value('port', 5).water
     
        # counters
        self.reward_drunk = 0
        self.led_intensity = 255


    def configure_gui(self): # Variables that appear in the GUI
        self.gui_input = ['trials_max']


    def main_loop(self):
        if self.trial_count < self.trials_with_same_side:
            pass
        elif self.trial_count < 2 * self.trials_with_same_side:
            if self.same_side_count == 0:

                self.side = "left" if self.side == "right" else "right"
                self.same_side_count = self.trials_with_same_side
            else:
                self.same_side_count -= 1
        else:

            self.side = random.choice(["left", "right"])


        self.trial_count += 1

        if self.side == "left":
            self.valvetime = self.valve_l_time
            self.valve_action = (Bpod.OutputChannels.Valve, 2)
            self.light_LED = (Bpod.OutputChannels.PWM2, self.led_intensity)
            self.poke_side= Bpod.Events.Port2In

        else:
            self.valvetime = self.valve_r_time
            self.valve_action = (Bpod.OutputChannels.Valve, 5)
            self.light_LED = (Bpod.OutputChannels.PWM5, self.led_intensity)
            self.poke_side= Bpod.Events.Port5In     



        ############ STATE MACHINE ################
        print('')
        print('Trial: ' + str(self.current_trial))
        print('Reward side: ' + str(self.side))




        self.sma.add_state(
            state_name='water_light',
            state_timer=self.valvetime,
            state_change_conditions={Bpod.Events.Tup: 'waiting_light'},
            output_actions=[self.light_LED, self.valve_action]
            )

        self.sma.add_state(
            state_name='waiting_light',
            state_timer=300,
            state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.poke_side: 'drink_delay'},
            output_actions=[self.light_LED]
            )

        self.sma.add_state(
            state_name='drink_delay',
            state_timer=2,
            state_change_conditions={Bpod.Events.Tup: 'exit'},
            output_actions=[])



    def after_trial(self):
        # Relevant prints
        self.register_value('side', self.side)








