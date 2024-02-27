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


class Test_Opto(Task):

    def __init__(self):
        super().__init__()


    def init_variables(self):

        self.trials_max = 100
        self.max_dur_light = 10
        self.pulse_pal = PulsePal(address='/dev/pulsepal')
        pulse1 = self.pulse_pal.create_square_pulse(self.max_dur_light, 0, 0, 3, samples_per_second=500)
        self.pulse_pal.assign_pulse(pulse1, 1)
        self.light_intensity = 10
        self.timer_off = 10


    def configure_gui(self):
        self.gui_input = ['trials_max', "light_intensity", "timer_off", "max_dur_light"]


    def main_loop(self):
        print('')
        print('Trial: ' + str(self.current_trial))

        self.time = self.timer_off / 2

        self.sma.add_state(
            state_name='Start_task',
            state_timer=self.timer,
            state_change_conditions={Bpod.Events.Tup: 'Light_on'},
            output_actions=[])



        self.sma.add_state(
            state_name='Light_on',
            state_timer=self.max_dur_light,
            state_change_conditions={Bpod.Events.Tup: 'Miss',
                                     #'Port1In': 'Correct',
                                     #'Port3In': 'Correct',
                                     #'Port4In': 'Correct',
                                     #'PA1_Port1In': 'Correct',
                                     #'PA1_Port2In': 'Correct',
                                     #'PA1_Port3In': 'Correct'
                                     },
            output_actions=[(Bpod.OutputChannels.BNC1, 3),
                            (Bpod.OutputChannels.PWM4, self.light_intensity),
                            #(Bpod.OutputChannels.LED, 4),
                            (Bpod.OutputChannels.SoftCode, 6)])

        self.sma.add_state(
            state_name='Miss',
            state_timer=self.timer,
            state_change_conditions={Bpod.Events.Tup: 'exit'},
            output_actions=[(Bpod.OutputChannels.SoftCode, 12)])

        #self.sma.add_state(
        #    state_name='Correct',
        #    state_timer=1,
        #    state_change_conditions={Bpod.Events.Tup: 'exit'},
        #    output_actions=[(Bpod.OutputChannels.BNC1, 0),
        #                   (Bpod.OutputChannels.SoftCode, 11)])



    def after_trial(self):
        self.register_value('reward_drunk', 0)



