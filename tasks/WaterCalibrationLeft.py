from academy.task_collection import Task
from pybpodapi.protocol import Bpod
from academy.utils import utils
from user import settings


class WaterCalibrationLeft(Task):
    def __init__(self):
        super().__init__()

        self.info = """
        Instructions of the task.
        Water and tolerance are measured in microliters.
        Weight is measured in grams.
        """

    def init_variables(self):
        self.trials_max = 100
        self.tolerance = 0.25

        self.interval = 1
        self.collection = utils.water_calibration
        self.ports = settings.BPOD_BEHAVIOR_PORTS_WATER

        self.port = [i for i, x in enumerate(self.ports) if x][0] + 1

        self.water = 3
        self.pulse_duration = 0.005

        item = self.collection.read_last_value('port', self.port)
        if item is not None:
            self.water = item.water
            self.pulse_duration = item.pulse_duration

        self.weight = 0
        self.min_pulse_duration = 0
        self.max_pulse_duration = 1000
        self.min_weight = 0 
        self.max_weight = 1000

        self.microliters_obtained = 0

        self.data_microliters = ''
        self.data_pulses = ''

        self.calibrated = False

    def configure_gui(self):
        self.gui_input = ['trials_max', 'interval', 'tolerance', 'water', 'weight']
        self.gui_output = ['port', 'pulse_duration', 'calibrated']

        self.microliters_obtained = self.weight * 1000 / self.trials_max

        if self.weight == 0:
            # first calibration, weight has not been introduced yet
            pass
        else:
            if self.data_microliters != '':
                self.data_microliters += ','
            self.data_microliters += str(self.microliters_obtained)
            if self.data_pulses != '':
                self.data_pulses += ','
            self.data_pulses += str(self.pulse_duration)


            if self.microliters_obtained - self.water > self.tolerance:
                self.max_weight = self.weight
                self.max_pulse_duration = self.pulse_duration

            elif self.microliters_obtained - self.water < -self.tolerance:
                self.min_weight = self.weight
                self.min_pulse_duration = self.pulse_duration
            else:
                self.calibrated = True
                self.collection.add_new_item({'port': self.port,
                                                'water': self.water,
                                                'pulse_duration': self.pulse_duration,
                                                'volumes': self.data_microliters,
                                                'pulses': self.data_pulses
                                                })
            if self.min_pulse_duration > 0 and self.max_pulse_duration < 1000:
                self.pulse_duration = self.bisection()
            else:
                self.pulse_duration = self.linear()

        print("duration of the pulse: ", self.pulse_duration)

    def main_loop(self):

        if not self.calibrated:

            print(self.current_trial)

            self.sma.add_state(
                state_name='Valve_on',
                state_timer=self.pulse_duration,
                state_change_conditions={Bpod.Events.Tup: 'Valve_off'},
                output_actions=[(Bpod.OutputChannels.Valve, str(int(self.port))), (Bpod.OutputChannels.LED, str(int(self.port)))])

            self.sma.add_state(
                state_name='Valve_off',
                state_timer=float(self.interval),
                state_change_conditions={Bpod.Events.Tup: 'exit'},
                output_actions=[])

    def after_trial(self):
        pass

    def linear(self):

        if self.min_pulse_duration > 0:
            duration = self.min_pulse_duration
            result = self.min_weight * 1000 / self.trials_max
        else:
            duration = self.max_pulse_duration
            result = self.max_weight * 1000 / self.trials_max

        target = self.water
        new_duration = round(duration * target / result, 4)

        return new_duration

    def bisection(self):
        result_high = self.max_weight * 1000 / self.trials_max
        result_low = self.min_weight * 1000 / self.trials_max
        result_target = self.water
        duration_high = self.max_pulse_duration
        duration_low = self.min_pulse_duration

        bis = (result_target - result_low) * (duration_high - duration_low) / (result_high - result_low) + duration_low
        new_duration = round(bis, 4)

        return new_duration
