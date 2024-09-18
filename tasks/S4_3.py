"""""
######  TASK INFO  #######

Teach mice to approach the central lickport to get the water reward

Starts with centre port LED ON. then side (L/R) water port LED ON + and it needs a nosepoke in the right lickport to get the automatic delivery of water.
All the LEDs stay ON until poke or timeup.

I this version, the first two blocks always start with the highest probabilities: random choice in between 0.9 and 0.1 and if 0.9 
reward right, then block 1 is going to be 0.1 so reward left and viceversa. 

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


class S4_3(Task):

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
        self.prob_right_values = [0.9,0.8,0.7]  # TO CHANGE if you want the prob_Right to be ONLY 0.8 and 0.2, then make this list prob_right_values = [0.8]
        
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
        
        self.outcome = ""

        # This function generates a vector with length N_blocks where each entry indicates the number of trials in that block
        # This function generates a vector with length N_blocks where each entry indicates the number of trials in that block
        # def generate_block_duration_vec(x_type, mean_x, N_blocks):
        #     # if (N_blocks % 2 == 0):
        #     # Warning('The number of blocks must be an even number')
        #     x = np.ndarray(shape=(N_blocks, 1), dtype=int)
        #     if x_type == "fixed":
        #         x[0:] = mean_x
        #     elif x_type == "exp":
        #         x = np.random.geometric(1 / mean_x, (N_blocks, 1))
        #         x = np.clip(x, 15, 45)  # TO CHANGE amplitude of the blocks
        #     else:
        #         Warning('Blocked type not supported')
        #     return x.flatten()

                # RANDOM UNIFORM DISTRIBUTION
        def generate_block_duration_vec(x_type, mean_x, N_blocks):
            x = np.ndarray(shape=(N_blocks, 1), dtype=int)
            if x_type == "fixed":
                x[0:] = mean_x
            elif x_type == "exp":
                mean_x = None 
                x = np.random.uniform(20, 55, (N_blocks, 1)).astype(int)
            else:
                Warning('Blocked type not supported')
            return x.flatten()

        def generate_probs_vec(N_blocks, prob_block_type, p_list, prob_Left_Right_blocks):

            # Force N_blocks to be even
            if (N_blocks % 2) == 1:
                N_blocks += 1
                warnings.warn('We increased the number of blocks by one to have an even number')
                print('N_blocks = ', N_blocks)

            N_probs = len(p_list)
            print('N_probs = ', N_probs)

            # Allocate memory for output_probs_vec
            output_probs_vec = np.ndarray(N_blocks, dtype=float)

            N_blocks_by_half = N_blocks // 2
            print('N_blocks_by_half = ', N_blocks_by_half)

            prob_list_Right_blocks = np.zeros(N_blocks_by_half, dtype=float)
            prob_list_Left_blocks = np.zeros(N_blocks_by_half, dtype=float)

            # Random choice between 0.9 and 0.1 for the first block
            first_block_prob = np.random.choice([0.9, 0.1])
            second_block_prob = 1.0 - first_block_prob  # The other value for the second block

            # Set the first block with the random choice and the second with the opposite
            output_probs_vec[0] = first_block_prob  # First block, random probability
            output_probs_vec[1] = second_block_prob  # Second block, the opposite

            # Reduce N_blocks by 2 to account for the first two blocks already assigned
            N_blocks -= 2
            N_blocks_by_half = N_blocks // 2

            if prob_block_type == 'rdm_values':
                # Generate random Right blocks
                prob_list_Right_blocks = np.random.choice(p_list, N_blocks_by_half) 
                # Generate Left blocks
                if prob_Left_Right_blocks == 'indep':
                    prob_list_Left_blocks = 1. - np.squeeze(np.random.choice(p_list, N_blocks_by_half))
                elif prob_Left_Right_blocks == 'balanced':
                    prob_list_Left_blocks = 1. - np.random.permutation(prob_list_Right_blocks)
                else:
                    warnings.warn('Specify the relation between Left and Right probs as balanced or indep')
                    return None  # Exit the function if input is invalid

            elif prob_block_type == 'permutation_prob_list':
                times_rep_per = N_blocks_by_half // N_probs
                print('times_rep_per = ', times_rep_per)
                for i in range(times_rep_per):
                    per_Right_probs = np.random.permutation(p_list)
                    per_Left_probs = 1. - np.random.permutation(p_list)
                    prob_list_Right_blocks[i * N_probs:(i + 1) * N_probs] = per_Right_probs
                    prob_list_Left_blocks[i * N_probs:(i + 1) * N_probs] = per_Left_probs

                remainder = N_blocks_by_half % N_probs
                if remainder > 0:
                    per_Right_probs = np.random.permutation(p_list)
                    per_Left_probs = 1. - np.random.permutation(p_list)
                    prob_list_Right_blocks[-remainder:] = per_Right_probs[:remainder]
                    prob_list_Left_blocks[-remainder:] = per_Left_probs[:remainder]

            else:
                warnings.warn('Specify the way to take prob values from prob_list: rdm_values or permutation_prob_list')
                return None  # Exit the function if input is invalid

            # Assign Right and Left blocks starting from the third block (index 2 onwards)
            rdm_right_block_order = np.random.permutation([0, 1])
            output_probs_vec[rdm_right_block_order[0] + 2::2] = prob_list_Right_blocks
            output_probs_vec[rdm_right_block_order[1] + 2::2] = prob_list_Left_blocks

            return output_probs_vec
        
    # This function generates a 2-column vector with length N_trials: where each entry indicates the prob_Right in that block
    # In colum 0, we specify the value on each trial of the prob_Right
    # In colum 1, we specify the binary value of where the reward is in that trial: =1 (reward on Right port), =0 (reward on Left port)

        def generate_blocked_reward_side_vec(N_blocks, block_duration_vec, probs_vec):
            # Initialize the output array
            x = np.zeros([1, 3])

            print(x)

            for i_block in range(N_blocks):
                # Convert the array entry block_duration_vec[i_block] into a scalar int
                bloc_dur = np.take(block_duration_vec[i_block], 0)

                # Column vector with the p_value of the block
                p = probs_vec[i_block] * np.ones((bloc_dur, 1), dtype=float)

                # Column vector with the rewarded sides of the block
                # If the probability is > 0.5, reward is on the right (1), otherwise left (0)
                if probs_vec[i_block] > 0.5:
                    # Reward goes to the right (1)
                    y = np.ones((bloc_dur, 1), dtype=int)
                else:
                    # Reward goes to the left (0)
                    y = np.zeros((bloc_dur, 1), dtype=int)

                # Create a column vector with the block number repeated for block duration
                blocks = np.repeat(i_block, bloc_dur).reshape(-1,1)

                # Concatenate probability, reward side, and block number
                Z = np.concatenate((p, y, blocks), axis=1)

                # Concatenate the current block to the previous blocks
                x = np.concatenate((x, Z), axis=0)

            # Remove the first row of x which contains zeros
            x = np.delete(x, 0, axis=0)
            print("x: " + str(x))
            return x
        
                # ITIs truncated exponential distribution 
        lambda_param = 0.3  # # TO CHANGE this is the mean of the distribution, (1/0.3 so 3,33 seconds)

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
            lambda_param = 0.3  # TO CHANGE lambda for exp distribution
            max_value = 30  # max value
            all_values = []
            for _ in range(num_trials):
                trial_values = generate_trial_values(lambda_param, max_value, num_values_per_trial)
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

        print("block_duration_vec: ", self.block_duration_vec)
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

        # input("escribe algo: ")

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
                self.correct_side = "left"#7
                self.wrong_side = "right"#1
                self.correct_poke_side = Bpod.Events.Port7In
                self.wrong_poke_side = Bpod.Events.Port1In
                self.valvetime = self.valve_l_time
                self.valve_action = (Bpod.OutputChannels.Valve, 7)
                self.poke_side = Bpod.Events.Port7In
            else:  # 1 per lato destro
                self.correct_side = "right"#1
                self.wrong_side = "left"#7
                self.correct_poke_side = Bpod.Events.Port1In
                self.wrong_poke_side = Bpod.Events.Port7In
                self.valvetime = self.valve_r_time
                self.valve_action = (Bpod.OutputChannels.Valve, 1)
                self.poke_side = Bpod.Events.Port1In


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

