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
import warnings
from scipy.signal import firwin, lfilter
import random


class S4_5(Task):

    def __init__(self):
        super().__init__()

    def init_variables(self):
        # general
        self.stage = 0
        self.substage = 0

        self.duration_max = 45*60  # 45 min finished the task 
        self.duration_min = 30*60  # 30 min door opens 

        self.trials_max = 16754
        self.N_blocks = 100
        self.prob_right_values = [0.9,0.8,0.7,0.6,0.5]  # TO CHANGE if you want the prob_Right to be ONLY 0.8 and 0.2, then make this list prob_right_values = [0.8]
        
        self.N_trials = 1000
        self.mean_x = 30
        self.trial_count = 0
        self.block_type = "exp"
        #self.block_type = "fixed" #block_type can take the categories 'fixed' and 'exp'
        # This can be rdm_values or permutation_prob_list
        self.prob_block_type = 'rdm_values'
        # self.prob_block_type ='permutation_prob_list'
        # prob_Left_Right_blocks can be 'balanced' meaning that the prob_Right in Right blocks is the same as the prob_Left on Left blocls
        # It can also be independent meaning that the prob_Right in Right blocks is INDEP of the prob_Left in Left blocks.
        # This can cause that in some sessions, the overall prob_R over the entire session is larger than 0.5
        self.prob_Left_Right_blocks = 'balanced'
        # self.prob_Left_Right_blocks = 'indep'

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

        # LED
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
        
        self.outcome = ""

        # This function generates a vector with length N_blocks where each entry indicates the number of trials in that block
        # This function generates a vector with length N_blocks where each entry indicates the number of trials in that block
        def generate_block_duration_vec(x_type, mean_x, N_blocks):
            # if (N_blocks % 2 == 0):
            # Warning('The number of blocks must be an even number')
            x = np.ndarray(shape=(N_blocks, 1), dtype=int)
            if x_type == "fixed":
                x[0:] = mean_x
            elif x_type == "exp":
                x = np.random.geometric(1 / mean_x, (N_blocks, 1))
                x = np.clip(x, 10, 50)  # TO CHANGE amplitude of the blocks
            else:
                Warning('Blocked type not supported')
            return x.flatten()

        # This function generates a vector with length N_blocks where each entry indicates the prob_Right in that block
        def generate_probs_vec(N_blocks, prob_block_type, p_list, prob_Left_Right_blocks):
            # N_trials = np.sum(block_duration_vec)
            # Allocate memory for the probs_vec array x
            x = np.ndarray(N_blocks, dtype=float)
            N_blocks_by_half = round(N_blocks / 2)
            prob_list_blocks135 = np.zeros(N_blocks_by_half, dtype=float)
            # blocks 1, 3, 5, 7 ... take values from
            rdm_right_block_order = np.random.permutation(
                [0, 1])  # the first position of this array rdm_right_block_order[0] ...
            # will determine which side is more probable in the first block
            # if rdm_right_block_order[0]=0 then the first block is a Right block , i.e. prob_Right > 0.5
            # if rdm_right_block_order[0]=1 then the first block is a Left block , i.e. prob_Right < 0.5

            # N_blocks_by_half= len(x[rdm_right_block_order[0]::2]) #we start the block in the rdm po
            if (prob_block_type == 'rdm_values'):
                prob_list_blocks135 = np.random.choice(p_list, N_blocks_by_half)
            elif (prob_block_type == 'permutation_prob_list'):
                per = np.random.permutation(p_list)
                N = len(per)
                times_rep_per = round(N_blocks_by_half / N)
                # we fill the prob_list_blocks135 array with as many repetitions from per as we can fit.
                for i in range(times_rep_per):
                    prob_list_blocks135[0 + i * N:0 + (i + 1) * N] = per
                # if the length N_blocks_by_half of the array prob_list_blocks135 is not a multiple of N, then we need to fill up the remainder of the entries of prob_list_blocks135
                for i in range(np.remainder(N_blocks_by_half, N)):
                    prob_list_blocks135[N * times_rep_per + i] = prob_list_blocks135[i]
            else:
                Warning('Specify the way to take prob values from prob_list: rdm_values or permutation_prob_list ')

            x[rdm_right_block_order[0]::2] = prob_list_blocks135

            # N_blocks_by_half= len(x[rdm_right_block_order[1]::2]) : if N_blocks is even, then the two halves of the x vector should have the same length
            if (
                    prob_Left_Right_blocks == 'indep'):  # in this condition, the Right and Left blocks have independent probabilities
                x[rdm_right_block_order[1]::2] = 1. - np.squeeze(np.random.choice(p_list, (N_blocks_by_half, 1)))
            elif (
                    prob_Left_Right_blocks == 'balanced'):  # in this condition, the Left blocks have 1 - p_Right but in a random order, so that the unconditional p_Right across the session is 0.5
                x[rdm_right_block_order[1]::2] = 1. - np.random.permutation(prob_list_blocks135)
            else:
                Warning('Specify the relation between Left and Right probs as balanced or indep')

            return x

            # This function generates a 2-column vector with length N_trials: where each entry indicates the prob_Right in that block
            # In colum 0, we specify the value on each trial of the prob_Right
            # In colum 1, we specify the binary value of where the reward is in that trial: =1 (reward on Right port), =0 (reward on Left port)

        def generate_blocked_reward_side_vec(N_blocks, block_duration_vec, probs_vec):
            # N_x = block_duration_vec.sum()
            # x = np.ndarray(shape= (N_x, 1), dtype = int)
            x = np.zeros([1, 3])

            print(x)

            for i_block in range(N_blocks):
                # we convert the array entry  block_duration_vec[i_block] into a scalar int or it will complain: "TypeError: only integer scalar arrays can be converted to a scalar index"
                bloc_dur = np.take(block_duration_vec[i_block], 0)

                # column vector with the p_value of the block
                p = probs_vec[i_block] * np.ones((bloc_dur, 1), dtype=float)

                # column vector with the rewarded sides of the block block_duration_vec[i_block]
                y = np.random.binomial(1, probs_vec[i_block], (bloc_dur, 1))

                # paste the two columns together
                blocks = np.repeat(i_block, bloc_dur).reshape(-1,1)

                Z = np.concatenate((p, y, blocks), axis=1)

                # conncateate the two-column vector of the block with previous blocks


                x = np.concatenate((x, Z), axis=0)

                # remove the first row of x which contains zeros
            x = np.delete(x, 0, axis=0)
            print("x: " + str(x))
            return x
        
                # ITIs truncated exponential distribution 
        lambda_param = 0.1  # # TO CHANGE this is the mean of the distribution, (1/0.1 so 10 seconds)

        # funtion to generate the truncated exponential distribution for the ITIs
        def generate_trial_values(lambda_param, max_value, num_values):
            trial_values = []
            for _ in range(num_values):
                while True:
                    value = random.expovariate(lambda_param)
                    if value <= max_value:
                        trial_values.append(value)
                        break
            return trial_values

        # function to obtain the values
        def custom_random_iti(num_trials, num_values_per_trial):
            lambda_parameter = 0.1  # TO CHANGE lambda for exp distribution
            max_value = 30  # max value
            all_values = []
            for _ in range(num_trials):
                trial_values = generate_trial_values(lambda_parameter, max_value, num_values_per_trial)
                all_values.extend(trial_values)
            return all_values

                #Generate the vector with the block duration (in trials)  for each block
        self.block_duration_vec = generate_block_duration_vec(x_type= self.block_type, mean_x= self.mean_x, N_blocks=self.N_blocks)

                #Generate the vector with the p_Right values for each block
        self.probs_vector = generate_probs_vec(self.N_blocks, self.prob_block_type , self.prob_right_values, self.prob_Left_Right_blocks)

                #Generate the binary vector with the Right (1) and Left (0) rewarded sides in each trial
        self.reward_side_vec_fixed_prob = generate_blocked_reward_side_vec(self.N_blocks, self.block_duration_vec, self.probs_vector)

                #Generate the vector tailored ITIs values (from 1 to 30 sec, mean=5 sec)
        self.random_iti_values = custom_random_iti(self.trials_max, 1)

        #print("block_duration_vec: ", self.block_duration_vec)
        #print("probs_vector: ", self.probs_vector)
        #print("reward_side_vec_fixed_prob: ", self.reward_side_vec_fixed_prob)
        #print("Tailored ITI values: ", self.random_iti_values)

    def configure_gui(self):  # Variables that appear in the GUI
        self.gui_input = ['trials_max']

    def main_loop(self):

        self.probability = self.reward_side_vec_fixed_prob[self.current_trial][0]
        self.reward_side_number = self.reward_side_vec_fixed_prob[self.current_trial][1]
        self.block_identity = self.reward_side_vec_fixed_prob[self.current_trial][2]
        self.random_iti = self.random_iti_values[self.current_trial]


        print("current_trial: ", self.current_trial)
        print("block_identity: ", self.block_identity)
        print("probability: ", self.probability)
        print("reward_side_number: ", self.reward_side_number)
        #print("ITI_duration: ", self.random_iti)


        if settings.BOX_NAME == 9:
            if self.reward_side_number == 0:  # 0 per lato sinistro
                self.correct_side = "left"
                self.wrong_side = "right"
                self.correct_poke_side = Bpod.Events.Port2In
                self.wrong_poke_side = Bpod.Events.Port5In
                self.valvetime = self.valve_l_time
                self.valve_action = (Bpod.OutputChannels.Valve, 2)
                self.poke_side = Bpod.Events.Port2In
            else:  # 1 per lato destro
                self.correct_side = "right"
                self.wrong_side = "left"
                self.correct_poke_side = Bpod.Events.Port5In
                self.wrong_poke_side = Bpod.Events.Port2In
                self.valvetime = self.valve_r_time
                self.valve_action = (Bpod.OutputChannels.Valve, 5)
                self.poke_side = Bpod.Events.Port5In
        
        elif settings.BOX_NAME == 12:
            if self.reward_side_number == 0:  # 0 per lato sinistro
                self.correct_side = "left"
                self.wrong_side = "right"
                self.correct_poke_side = Bpod.Events.Port1In
                self.wrong_poke_side = Bpod.Events.Port7In
                self.valvetime = self.valve_l_time
                self.valve_action = (Bpod.OutputChannels.Valve, 1)
                self.poke_side = Bpod.Events.Port1In
            else:  # 1 per lato destro
                self.correct_side = "right"
                self.wrong_side = "left"
                self.correct_poke_side = Bpod.Events.Port7In
                self.wrong_poke_side = Bpod.Events.Port1In
                self.valvetime = self.valve_r_time
                self.valve_action = (Bpod.OutputChannels.Valve, 7)
                self.poke_side = Bpod.Events.Port7In



        ############ STATE MACHINE ################

        print('Reward side: ' + str(self.correct_side))
        print('')


        # Only the first trial
        if self.current_trial == 0:
            self.sma.add_state(
                state_name='center_light',
                state_timer= 0,
                state_change_conditions={self.centre_poke: 'side_light'},
                output_actions=[self.centre_light_LED] 
            )

            self.sma.add_state(
                state_name='side_light',
                state_timer= 10,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'water_delivery',
                                        self.wrong_poke_side: 'wrong_side'},
                output_actions=[self.light_l_LED, self.light_r_LED, (Bpod.OutputChannels.SoftCode, 20)] #softcode 20 to close door2
            )
            
        else:
            self.sma.add_state(
                state_name='center_light',
                state_timer= 1000,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.centre_poke: 'side_light'},
                output_actions=[self.centre_light_LED]
            )

            self.sma.add_state(
                state_name='side_light',
                state_timer= 10,
                state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'water_delivery',
                                        self.wrong_poke_side: 'wrong_side'},
                output_actions=[self.light_l_LED, self.light_r_LED]
            )

        self.sma.add_state(
            state_name='water_delivery',
            state_timer=self.valvetime,
            state_change_conditions={Bpod.Events.Tup: 'drink_delay', self.correct_poke_side: 'drink_delay'},
            output_actions=[self.valve_action]
        )

        self.sma.add_state(
            state_name='wrong_side',
            state_timer=0.5,
            state_change_conditions={Bpod.Events.Tup: 'drink_delay'},
            output_actions=[(Bpod.OutputChannels.SoftCode, 1)]
        )


        self.sma.add_state(
            state_name='drink_delay',
            state_timer=self.random_iti,
            state_change_conditions={Bpod.Events.Tup: 'exit'},
            output_actions=[]
        )




    def after_trial(self):

        if self.current_trial_states['water_delivery'][0][0] > 0: # check that the animal went to that state
            self.outcome = "correct"
            if self.correct_side == 'left':
                self.reward_drunk += self.valve_l_reward 
            else:
                self.reward_drunk += self.valve_r_reward 
            
        elif self.current_trial_states['wrong_side'][0][0] > 0: #
            self.outcome = "incorrect"

        elif self.current_trial_states['side_light'][0][0] > 0: 
            self.outcome = "miss"

        else:
            self.outcome = "omision"






        # Relevant prints
        self.register_value('side', self.correct_side)
        self.register_value('probability_r', self.probability)
        self.register_value('Block_index', self.block_identity)
        self.register_value('Block_type', self.block_type)
        self.register_value('Prob_block_type', self.prob_block_type)
        self.register_value('Probability_L_R_blocks', self.prob_Left_Right_blocks)
        self.register_value('list_prob_R_values', self.prob_right_values)
        self.register_value('outcome', self.outcome)
        self.register_value('reward_drunk', self.reward_drunk)
        self.register_value('iti_duration', self.random_iti)

