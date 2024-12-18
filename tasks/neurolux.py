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


class neurolux(Task):

    def __init__(self):
        super().__init__()

    def init_variables(self):
        # general
        self.stage = 0
        self.substage = 0
        self.trials_max = 167544357423
        self.side = random.choice(["left", "right"])
        self.trial_count = 0
        output_actions=[
            (self.side,),
            (Bpod.OutputChannels.SoftCode, 20)
        ]
        self.duration_max = 45*60  # 45 min finished the task 
        self.duration_min = 30*60  # 30 min door opens 

        # pumps
        if settings.BOX_NAME == 9:
            self.valve_l_time = utils.water_calibration.read_last_value('port', 2).pulse_duration
            self.valve_l_reward = utils.water_calibration.read_last_value('port', 2).water
            self.valve_r_time = utils.water_calibration.read_last_value('port', 5).pulse_duration
            self.valve_r_reward = utils.water_calibration.read_last_value('port', 5).water
        elif settings.BOX_NAME == 12:
            self.valve_l_time = utils.water_calibration.read_last_value('port', 1).pulse_duration
            self.valve_l_reward = utils.water_calibration.read_last_value('port', 1).water
            self.valve_r_time = utils.water_calibration.read_last_value('port', 7).pulse_duration
            self.valve_r_reward = utils.water_calibration.read_last_value('port', 7).water

        # counters
        self.reward_drunk = 0
        self.led_intensity = 255

        # centre_light_LED
        if settings.BOX_NAME == 9:
            self.centre_light_LED = (Bpod.OutputChannels.PWM3, self.led_intensity)
            self.centre_poke = (Bpod.Events.Port3In)
            self.light_l_LED = (Bpod.OutputChannels.PWM2, self.led_intensity)
            self.light_r_LED = (Bpod.OutputChannels.PWM5, self.led_intensity)
        
        elif settings.BOX_NAME == 12:
            self.centre_light_LED = (Bpod.OutputChannels.PWM4, self.led_intensity)
            self.centre_poke = (Bpod.Events.Port4In)
            self.light_l_LED = (Bpod.OutputChannels.PWM1, self.led_intensity)
            self.light_r_LED = (Bpod.OutputChannels.PWM7, self.led_intensity)

        #print("hola")

        
    def configure_gui(self):  # Variables that appear in the GUI
        self.gui_input = ['trials_max']

    def main_loop(self):

        random_number = random.randint(0, 1)

        if random_number == 1:
            self.side = "left"
            side_led_on = self.light_l_LED
            self.valvetime = self.valve_l_time
            self.correct_side = self.side
            self.wrong_side = "right"

        else:
            self.side = "right"
            side_led_on = self.light_r_LED
            self.valvetime = self.valve_r_time
            self.correct_side = self.side
            self.wrong_side = "left"


        if settings.BOX_NAME == 9:
            if self.side == "left":
                self.correct_poke_side= Bpod.Events.Port2In
                self.wrong_poke_side = Bpod.Events.Port5In
                self.valve_action = (Bpod.OutputChannels.Valve, 2)
                self.poke_side = Bpod.Events.Port2In

            else:
                self.side = "right"
                self.correct_poke_side= Bpod.Events.Port5In
                self.wrong_poke_side = Bpod.Events.Port2In
                self.valve_action = (Bpod.OutputChannels.Valve, 5)
                self.poke_side = Bpod.Events.Port5In

        elif settings.BOX_NAME == 12:
            if self.side == "left": #7
                self.correct_side = self.side
                self.wrong_side = "right" #1
                self.correct_poke_side= Bpod.Events.Port7In
                self.wrong_poke_side = Bpod.Events.Port1In
                self.valvetime = self.valve_l_time
                self.valve_action = (Bpod.OutputChannels.Valve, 7)
                self.poke_side = Bpod.Events.Port7In

            else:
                self.correct_side = self.side
                self.wrong_side = "left" #7
                self.correct_poke_side= Bpod.Events.Port1In
                self.wrong_poke_side = Bpod.Events.Port7In
                self.valvetime = self.valve_r_time
                self.valve_action = (Bpod.OutputChannels.Valve, 1)
                self.poke_side = Bpod.Events.Port1In

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

            self.sma.add_state(
                state_name='side_light',
                state_timer=10,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'water_delivery',
                                        self.wrong_poke_side: 'wrong_side'},
                output_actions=[side_led_on, (Bpod.OutputChannels.SoftCode, 20)] #softcode 20 to close door2
            ) 

        else:
            self.sma.add_state(
                state_name='center_light',
                state_timer=10000,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.centre_poke: 'side_light'},
                output_actions=[self.centre_light_LED]
            )

            self.sma.add_state(
                state_name='side_light',
                state_timer=10,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'water_delivery',
                                        self.wrong_poke_side: 'wrong_side'},
                output_actions=[side_led_on] 
            ) 
            #print("hola5")

        self.sma.add_state(
            state_name='water_delivery',
            state_timer=self.valvetime,
            state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'drink_delay'},
            output_actions=[self.valve_action]
        )

        self.sma.add_state(
            state_name='wrong_side',
            state_timer=0,
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
            state_timer=2,
            state_change_conditions={Bpod.Events.Tup: 'exit'},
            output_actions=[]
        )


    def after_trial(self):

        if self.current_trial_states['water_delivery'][0][0] > 0: # check that the animal went to that state
            if self.side == "left":
                self.reward_drunk += self.valve_l_reward
            else:
                self.reward_drunk += self.valve_r_reward


        # Relevant prints
        self.register_value('side', self.side)
        self.register_value('reward_drunk', self.reward_drunk)
