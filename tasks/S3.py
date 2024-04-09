"""""
######  TASK INFO  #######

Teach mice to approach the central lickport to get the water reward

Starts with centre port LED ON. then side (L/R) water port LED ON + and it needs a nosepoke in the right lickport to get the automatic delivery of water.
All the LEDs stay ON until poke or timeup.

######  PORTS INFO  #######

Port 1 - Right port
Port 3 - Central port
Port 5 - Left port

"""""
from academy.task_collection import Task
from pybpodapi.protocol import Bpod
from academy.utils import utils
from user import settings
import random
import numpy as np
from scipy.signal import firwin, lfilter


class S3(Task):

    def __init__(self):
        super().__init__()

    def init_variables(self):
        # general
        self.stage = 0
        self.substage = 0
        self.trials_max = 167544357423
        self.side = random.choice(["left", "right"])
        self.trials_with_same_side = 20
        self.trial_count = 0
        self.same_side_count = 0
        output_actions=[
            (self.side,),
            (Bpod.OutputChannels.SoftCode, 20)
        ]


        # pumps
        self.valve_r_time = utils.water_calibration.read_last_value('port', 2).pulse_duration
        self.valve_r_reward = utils.water_calibration.read_last_value('port', 2).water
        self.valve_l_time = utils.water_calibration.read_last_value('port', 5).pulse_duration
        self.valve_l_reward = utils.water_calibration.read_last_value('port', 5).water

        # counters
        self.reward_drunk = 0
        self.led_intensity = 255

        # centre_light_LED
        self.centre_light_LED = (Bpod.OutputChannels.PWM3, self.led_intensity)
        self.centre_poke = (Bpod.Events.Port3In)
        self.light_l_LED = (Bpod.OutputChannels.PWM2, self.led_intensity)
        self.light_r_LED = (Bpod.OutputChannels.PWM5, self.led_intensity)

        print("hola")

        
    def configure_gui(self):  # Variables that appear in the GUI
        self.gui_input = ['trials_max']

    def main_loop(self):
        if self.trial_count < self.trials_max:

            if self.trial_count % self.trials_with_same_side == 0:

                self.side = "left" if self.side == "right" else "right"

            self.trial_count += 1
        print("hola1")
        if self.side == "left":
            self.correct_side = self.side
            self.wrong_side = "right"
            self.correct_poke_side= Bpod.Events.Port2In
            self.wrong_poke_side = Bpod.Events.Port5In
            self.valvetime = self.valve_l_time
            self.valve_action = (Bpod.OutputChannels.Valve, 2)
            self.poke_side = Bpod.Events.Port2In
            print("hola2")
        else:
            self.correct_side = self.side
            self.wrong_side = "left"
            self.correct_poke_side= Bpod.Events.Port5In
            self.wrong_poke_side = Bpod.Events.Port2In
            self.valvetime = self.valve_r_time
            self.valve_action = (Bpod.OutputChannels.Valve, 5)
            self.poke_side = Bpod.Events.Port5In
            print("hola3")
        ############ STATE MACHINE ################

        print('')
        print('Trial: ' + str(self.current_trial))
        print('Reward side: ' + str(self.side))

        if self.current_trial == 0:
            self.sma.add_state(
                state_name='center_light',
                state_timer=0,
                state_change_conditions={self.centre_poke: 'side_light'},
                output_actions=[self.centre_light_LED]
            )
            print("hola4")
            self.sma.add_state(
                state_name='side_light',
                state_timer=10,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'water_delivery',
                                        self.wrong_poke_side: 'wrong_side'},
                output_actions=[self.light_l_LED, self.light_r_LED, (Bpod.OutputChannels.SoftCode, 20)] #softcode 20 to close door2
            ) 
            print("hola5")
        else:
            self.sma.add_state(
                state_name='center_light',
                state_timer=300,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.centre_poke: 'side_light'},
                output_actions=[self.centre_light_LED]
            )

            self.sma.add_state(
                state_name='side_light',
                state_timer=300,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'water_delivery',
                                        self.wrong_poke_side: 'wrong_side'},
                output_actions=[self.side]
            )

        self.sma.add_state(
            state_name='water_delivery',
            state_timer=self.valvetime,
            state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'drink_delay'},
            output_actions=[self.valve_action]
        )

        self.sma.add_state(
            state_name='wrong_side',
            state_timer=2,
            state_change_conditions={Bpod.Events.Tup: 'timeout'},
            output_actions=[(Bpod.OutputChannels.SoftCode, 1)]
        )

        self.sma.add_state(
            state_name='timeout',
            state_timer=2,
            state_change_conditions={Bpod.Events.Tup: 'exit'},
            output_actions=[(Bpod.OutputChannels.SoftCode, 2)]
        )

        self.sma.add_state(
            state_name='drink_delay',
            state_timer=1,
            state_change_conditions={Bpod.Events.Tup: 'exit'},
            output_actions=[]
        )


    def after_trial(self):
        # Relevant prints
        self.register_value('side', self.side)

