from academy.task_collection import Task
from pybpodapi.protocol import Bpod
from academy.utils import utils
from user import settings
import random
import numpy as np
if settings.PULSEPAL_CONNECTED:
    from academy.pulse_pal import PulsePal
else:
    print('Not pulsepal found')
    from academy.pulse_pal import FakePulsePal as PulsePal


class Test_opto_single(Task):

    def __init__(self):
        super().__init__()


    def init_variables(self):

        self.trials_max = 100
        self.max_dur_light = 2
        self.pulse_pal = PulsePal(address='/dev/pulsepal')

        self.led_intensity = 255

                # LED
        if settings.BOX_NAME == 9:
            self.centre_light_LED = (Bpod.OutputChannels.PWM3, self.led_intensity)
            self.centre_poke = (Bpod.Events.Port3In)
            self.light_l_LED = (Bpod.OutputChannels.PWM2, self.led_intensity)
            self.light_r_LED = (Bpod.OutputChannels.PWM5, self.led_intensity)
        
        elif settings.BOX_NAME == 12:
            self.centre_light_LED = (Bpod.OutputChannels.PWM4, self.led_intensity)
            self.centre_poke = (Bpod.Events.Port4In)
            self.light_l_LED = (Bpod.OutputChannels.PWM7, self.led_intensity)
            self.light_r_LED = (Bpod.OutputChannels.PWM1, self.led_intensity)

        


    def configure_gui(self):
        self.gui_input = ["trials_max", "max_dur_light"]


    def main_loop(self):
        self.max_dur_light = 1


        # luz continua
        pulse1 = self.pulse_pal.create_square_pulse(self.max_dur_light, 0, 0.2, 5)
        self.pulse_pal.assign_pulse(pulse1, 1)

        # pulse2 = self.pulse_pal.create_square_pulse(0.2, 0, 0.2, 5)
        # self.pulse_pal.assign_pulse(pulse2, 2) #use it if ypu need to stop the pulse before one sec (or the regular duration) 


        # tren de pulsos
        #pulse1 = self.pulse_pal.create_square_pulsetrain(self.max_dur_light, 0.005, 0.045, 5)
        #self.pulse_pal.assign_pulse(pulse1, 1)

        #pulse2 = self.pulse_pal.create_square_pulse(0, 0, 0, 5)
        #self.pulse_pal.assign_pulse(pulse2, 2)




        self.sma.add_state(
            state_name='Start_task',
            state_timer=2,
            state_change_conditions={Bpod.Events.Tup: 'Light_on'},
            output_actions=[])


        self.sma.add_state(
            state_name='Light_on',
            state_timer=1,
            state_change_conditions={Bpod.Events.Tup: 'Light_off'},
            output_actions=[(Bpod.OutputChannels.SoftCode, 6), self.centre_light_LED])

        self.sma.add_state(
            state_name='Light_off',
            state_timer=3,
            state_change_conditions={Bpod.Events.Tup: 'exit'},
            output_actions=[(Bpod.OutputChannels.SoftCode, 7)])

    def after_trial(self):
        self.register_value('reward_drunk', 0)



