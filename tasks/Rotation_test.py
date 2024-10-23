from academy.task_collection import Task
from pybpodapi.protocol import Bpod
from pybpodapi.bpod.hardware.output_channels import OutputChannel
from user import settings

#if settings.PULSEPAL_CONNECTED:
#    from academy.pulse_pal import PulsePal
#else:
#    print('Not pulsepal found')
#    from academy.pulse_pal import FakePulsePal as PulsePal

# GENERAL INFO:
# The code intereleave light off on every 3 seconds.
# Trials_max will indicate the number fo repetitions of the off on states (by default 1)
# Max duration light: indicates the maximum time that the opto stimulatio is on every time enters in this state.
#   if you want to extend it remove (Bpod.OutputChannels.SoftCode, 7) from ligt_off state
# Led_intensity. Central port LED will turn on in sinchrony with the light stimuluation for better visualization.
#   if you don't want illumination led_intensity=0

class Rotation_test(Task):

    def __init__(self):
        super().__init__()

    def init_variables(self):

        self.trials_max = 50
        self.max_dur_light = 5
        #self.pulse_pal = PulsePal(address='/dev/pulsepal')
        self.led_intensity = 255 #enough to be detected by the video but not to scare the mouse

        # LED
        if settings.BOX_NAME == 9: #SETUP MV 4A
            self.centre_light_LED = (Bpod.OutputChannels.PWM3, self.led_intensity)

        elif settings.BOX_NAME == 4: #SETUP MV3A
            self.centre_light_LED = (Bpod.OutputChannels.PWM3, self.led_intensity)

        elif settings.BOX_NAME == 12: #SETUP OPTO 4A
            self.centre_light_LED = (Bpod.OutputChannels.PWM4, self.led_intensity)


    def configure_gui(self):
        self.gui_input = ["trials_max", "max_dur_light", "led_intensity"]

    def main_loop(self):

        #TRAIN PULSE
        #pulse 1 is a pulse (continuous or pulse train) with a maximum duration = self.max_dur_light
        #pulse1 = self.pulse_pal.create_square_pulsetrain(self.max_dur_light, 0.002, 0.048, 5)  #duration, time_on, time_off, voltage, samples_per_second= 1000
        #self.pulse_pal.assign_pulse(pulse1, 1)

        # #PULSE to STOP
        # # pulse 2 is a pulse we can send to stop the pulse1 before the maximum duration
        # pulse2 = self.pulse_pal.create_square_pulse(0, 0, 0, 5) #duration, duration_ramp_in, duration_ramp_off, voltage, samples_per_second= 1000
        # self.pulse_pal.assign_pulse(pulse2, 2)

        self.sma.add_state(
            state_name='Light_off',
            state_timer=self.max_dur_light,
            state_change_conditions={Bpod.Events.Tup: 'Light_on'},
            output_actions=[(Bpod.OutputChannels.BNC1, 0), 
                            (Bpod.OutputChannels.SoftCode, 7), 
                            (Bpod.OutputChannels.PWM2, self.led_intensity),
                            (Bpod.OutputChannels.PWM3, self.led_intensity),
                            (Bpod.OutputChannels.PWM5, self.led_intensity)]) 

        self.sma.add_state(
            state_name='Light_on',
            state_timer=self.max_dur_light,
            state_change_conditions={Bpod.Events.Tup: 'exit'},
            output_actions=[(Bpod.OutputChannels.BNC1, 3), 
                            (Bpod.OutputChannels.SoftCode, 6), 
                            (Bpod.OutputChannels.PWM2, self.led_intensity),
                            (Bpod.OutputChannels.PWM3, self.led_intensity),
                            (Bpod.OutputChannels.PWM5, self.led_intensity)]) #pulse 1

    def after_trial(self):
        pass



