import numpy as np
from academy import telegram_bot
from user import settings

# Examples of functions to calculate new task and stage
# If the function fails to return, new task and stage will be previous task and previous stage
# df is the session dataframe for the subject


def select_task(df, subject):
    print('start')


    # variables by default
    task = subject.task
    wait_seconds = 3600 * settings.TIME_TO_ENTER  # wait a minimum of x hours before allowed to start the new session)

    #Long time to enter for certain subjects
    if df.subject.iloc[0] in settings.LONGER_TIME_TO_ENTER:
        wait_seconds = 3600 * 72  #longer times for lazy animals
        print('Longer time to enter!')


    stage = float(subject.stage)
    substage = float(subject.substage)
    choice = subject.choice
    stim_dur_ds= 0
    stim_dur_dm= 0
    stim_dur_dl= 0

    print('01')
    last_session = df.session.max()
    df_last_session = df.loc[df['session'] == last_session].copy()         
    n_trials_last_session = df_last_session.trial.max()  # number of trials in current session

    #df_last3 = df.loc[df['session'] > last_session - 3].copy()
    #last3_total_trials = df_last3.groupby('session')['trial'].max()  #list of the total trials performed in the last 5 sessions
    #sessions_above_250_trials = sum(1 for value in last3_total_trials if value > 250)

    sessions_in_S2 = df.loc[df['task'] == 'S2'].copy()
    sessions_in_S2_total_trials = sessions_in_S2.groupby('session')['trial'].max() 
    sessions_in_S2_above_250_trials = sum(1 for value in sessions_in_S2_total_trials if value >  170)

    sessions_in_S3 = df.loc[df['task'] == 'S3'].copy()
    sessions_in_S3_total_trials = sessions_in_S3.groupby('session')['trial'].max() 
    sessions_in_S3_above_250_trials = sum(1 for value in sessions_in_S3_total_trials if value > 170)

    sessions_in_S4_1 = df.loc[df['task'] == 'S4_1'].copy()
    sessions_in_S4_1_total_trials = sessions_in_S4_1.groupby('session')['trial'].max() 
    sessions_in_S4_1_above_250_trials = sum(1 for value in sessions_in_S4_1_total_trials if value >  170)
    
    sessions_in_S4_2 = df.loc[df['task'] == 'S4_2'].copy()
    sessions_in_S4_2_total_trials = sessions_in_S4_2.groupby('session')['trial'].max() 
    sessions_in_S4_2_above_250_trials = sum(1 for value in sessions_in_S4_2_total_trials if value >  170)

    sessions_in_S4_3 = df.loc[df['task'] == 'S4_3'].copy()
    sessions_in_S4_3_total_trials = sessions_in_S4_3.groupby('session')['trial'].max() 
    sessions_in_S4_3_above_250_trials = sum(1 for value in sessions_in_S4_3_total_trials if value >  170)

    sessions_in_S4_4 = df.loc[df['task'] == 'S4_4'].copy()
    sessions_in_S4_4_total_trials = sessions_in_S4_4.groupby('session')['trial'].max() 
    sessions_in_S4_4_above_250_trials = sum(1 for value in sessions_in_S4_4_total_trials if value >  170)

    print('02')
    if task == "S1":
        task = "S2"

    elif task == "S2":
        if sessions_in_S2_above_250_trials >= 1:
            task = "S3"
        else:
            task ="S2"
            
    elif task == "S3":
        if sessions_in_S3_above_250_trials >= 1:
                task = "S4_1"
        else:
            task = "S3"
    
    elif task == "S4_1":
        if sessions_in_S4_1_above_250_trials >=4:
           task = "S4_2"
        else:
            task = "S4_1"
    
    elif task == "S4_2":
        if sessions_in_S4_2_above_250_trials >=4:
           task = "S4_3"
        else:
            task == "S4_2"

    elif task == "S4_3":
        if sessions_in_S4_3_above_250_trials >=4:
           task = "S4_4"
        else:
            task == "S4_3"
    
    elif task == "S4_4":
        if sessions_in_S4_4_above_250_trials >=4:
           task = "S4_5"
        else:
            task == "S4_4"
    
    elif task == "S4_5":
        print('03')
        task = "S4_5"

    else:
        print('04')
        task = "S4_5"

    return task, stage, substage, wait_seconds, stim_dur_ds, stim_dur_dm, stim_dur_dl, choice



wait_seconds = 3600*settings.TIME_TO_ENTER  # wait a minimum of x hours before allowed to start the new session)
print('05')














# # dataframes
#     last_session = df.session.max()
#     df_last5 = df.loc[df['session'] > last_session - 5].copy()  # last five sessions
#     df_last3 = df.loc[df['session'] > last_session - 3].copy()  # last three sessions
#     df_last2 = df.loc[df['session'] > last_session - 2].copy()  # last two sessions
#     df = df.loc[df['session'] == last_session].copy()           # last session

#     # number of trials
#     n_trials = df.trial.max()  # number of trials in current session
#     n_trials_prev = df_last2.groupby('session')['trial'].max().values[0]  # number of trials in previous session

#     #setup
#     setup = df.box.unique()



#     if task == 'Automatic_Water': # We want to rcover previous sessions parameters after this emergency water stage
#         prev_session = df.loc[df['session'] == last_session - 2].iloc[-1]
#         wait_seconds = 3600 * 5
#         task = prev_session.task
#         stage = float(prev_session.stage)
#         substage = float(prev_session.substage)
#         stim_dur_ds = float(prev_session.stim_dur_ds)
#         stim_dur_dm = float(prev_session.stim_dur_dm)
#         stim_dur_dl= float(prev_session.stim_dur_dl)

#     elif task == 'Habituation':
#         wait_seconds = 3600 * 1
#         if len(df_last2.session.unique())>=2: # Pass after 2 sessions
#             task = 'LickTeaching'

#     elif task == 'LickTeaching':
#         wait_seconds = 3600 * 2
#         if n_trials > 55:
#             task = 'TouchTeaching'

#     elif task == 'TouchTeaching':
#         if n_trials >= 50:
#             if setup==4:  #MV1
#                 task = 'StageTraining_10B_V3'
#             elif setup == 3:  #MV2
#                 task = 'StageTraining_10B_V1'
#             elif setup==5: # MV3
#                 task = 'StageTraining_9B_V2'
#             stage = float(1)
#             substage = float(1)

#     elif 'StageTraining' in task:
#         ############################ FUNTIONS ############################
#         def func(x):
#             if x.last_valid_index() is None:
#                 return None
#             else:
#                 return x[x.last_valid_index()]

#         def variable_calc(variable, initial, final):
#             "calculates the average between initial and final values of a changing variable"
#             try:
#                 init = df[variable].iloc[10]
#                 fin = df[variable].iloc[-1]
#             except:  # very short session, pick previous session value
#                 try:
#                     previous = df_last2.loc[df_last2['session'] < last_session].copy()
#                     init = previous[variable].iloc[10]
#                     fin = previous[variable].iloc[-1]
#                 except:  # 2 very short sessions pick the easiest value
#                     init = initial
#                     fin = final
#             average = (init + fin) / 2
#             return (average, init)

#         ############################ SMALL PARSING ############################

#         #number of trials
#         if n_trials < 15:
#             my_subject = df.subject.iloc[0]
#             if my_subject not in settings.INACTIVE_SUBJECTS:
#                 telegram_bot.alarm_few_trials(n_trials, my_subject)

#         # get first and last responses
#         sort = df['response_x'].astype(str).str.split(',', expand=True) # separate reponses in columns
#         df['first_resp'] = sort[0].astype(float)                        # select first reponses
#         df['last_resp'] = sort.apply(func, axis=1).astype(float)        # select last reponses
#         # useful columns
#         df['first_error'] = df['first_resp'] - df['x']  # error calculation
#         df['last_error'] = df['last_resp'] - df['x']
#         df['first_correct_bool'] = np.where(df['correct_th'] / 2 >= df['first_error'].abs(), 1, 0)  # correct bool calc
#         df['last_correct_bool'] = np.where(df['correct_th'] / 2 >= df['last_error'].abs(), 1, 0)
#         df.loc[(df.trial_result == 'miss', ['first_correct_bool', 'last_correct_bool'])] = np.nan  # misses correction

#         # last 3
#         sort_last3 = df_last3['response_x'].astype(str).str.split(',', expand=True)
#         df_last3['first_resp'] = sort_last3[0].astype(float)
#         df_last3['last_resp'] = sort_last3.apply(func, axis=1).astype(float)
#         df_last3['first_error'] = df_last3['first_resp'] - df_last3['x']
#         df_last3['last_error'] = df_last3['last_resp'] - df_last3['x']
#         df_last3['first_correct_bool'] = np.where(df_last3['correct_th'] / 2 >= df_last3['first_error'].abs(), 1, 0)
#         df_last3['last_correct_bool'] = np.where(df_last3['correct_th'] / 2 >= df_last3['last_error'].abs(), 1, 0)

#         # last 5
#         sort_last5 = df_last5['response_x'].astype(str).str.split(',', expand=True)
#         df_last5['first_resp'] = sort_last5[0].astype(float)
#         df_last5['last_resp'] = sort_last5.apply(func, axis=1).astype(float)
#         df_last5['first_error'] = df_last5['first_resp'] - df_last5['x']
#         df_last5['last_error'] = df_last5['last_resp'] - df_last5['x']
#         df_last5['last_correct_bool'] = np.where(df_last5['correct_th'] / 2 >= df_last5['last_error'].abs(), 1, 0)
#         df_last5['first_correct_bool'] = np.where(df_last5['correct_th'] / 2 >= df_last5['first_error'].abs(), 1, 0)

#         # last substages lists
#         last3_stages = df_last3.stage.unique()
#         last3_substages = df_last3.substage.unique()
#         last5_substages = df_last5.substage.unique()

#         # accuracies calc
#         first_poke_acc = df.first_correct_bool.mean()
#         last_poke_acc = df.last_correct_bool.mean()
#         first3_poke_acc = df_last3.first_correct_bool.mean()
#         last3_poke_acc = df_last3.last_correct_bool.mean()
#         first5_poke_acc = df_last5.first_correct_bool.mean()
#         last5_poke_acc = df_last5.last_correct_bool.mean()

#         # subdataframes
#         vg_df = df.loc[df['trial_type'] == 'VG']
#         ds_df = df.loc[((df['trial_type'] == 'DS') | (df['trial_type'] == 'DSc1') | (df['trial_type'] == 'DSc2'))]
#         dm_df = df.loc[((df['trial_type'] == 'DM') | (df['trial_type'] == 'DMc1'))]
#         dl_df = df.loc[((df['trial_type'] == 'DL'))]


#         ############################ STAGE & SUBSTAGE SELECTION ############################

#         ########## OPTO ############
#         try:
#             df.subject.iloc[0]
#             if df.opto_type.iloc[-1]== 6 or df.opto_type.iloc[-1]== 7:  # 0 off, 6 for inhibition, 7 for activation
#                 choice = 0
#             elif df.opto_type.iloc[-1] == 0:
#                 choice = 6
#         except:
#             choice = 0

#         #choice = 0  # REMOVE THIS !!!!!!

#         ############ STAGE 1 ############
#         if stage == 1:
#             if substage == 1:
#                 if last3_poke_acc >= 0.8 and len(last5_substages) == 1 and n_trials > 60:  # next substage
#                     substage += 1
#                 # elif n_trials <= 15 and len(last5_substages) == 1:  # go to Touchteaching
#                 #     task = 'TouchTeaching'
#                 #     stage -= 1
#                 #     substage -= 1

#             elif substage == 2:
#                 stim_pos_acc = vg_df.groupby('x')['first_correct_bool'].mean() # accuracy by stimulus in VG trials
#                 stim_pos_acc.to_list()
#                 if all(i >= 0.7 for i in stim_pos_acc) and len(last5_substages) == 1 and n_trials > 60 and first3_poke_acc >0.65:  # next substage
#                     substage += 1
#                 elif first_poke_acc <= 0.33 and len(last3_substages) == 1:  # lower substage
#                     substage -= 1

#             elif substage == 3:
#                 acc_ds = ds_df['first_correct_bool'].mean() # accuracy in delay short
#                 if acc_ds >= 0.55 and len(last5_substages) == 1 and n_trials > 60 and first3_poke_acc >0.7:  # next stage
#                     stage += 1
#                     substage = float(1)
#                     stim_dur_ds = 0.45
#                 elif first_poke_acc < 0.35 and len(last3_substages) == 1 :  # lower substage
#                     substage -= 1

#         ############ STAGE 2 ############
#         elif stage == 2:
#             next_stage = False
#             lower_stage = False
#             if substage == 1:
#                 max_stim_dur = 0.45
#                 average, initial = variable_calc('stim_dur_ds', max_stim_dur, max_stim_dur)
#                 acc = ds_df['first_correct_bool'].mean()
#                 last3_stim_dur = df_last3.loc[df_last3['trial'] == 10]['stim_dur_ds'].median()
#                 acc_up = 0.6
#                 acc_down = 0.45
#                 change = 0.075
#             elif substage ==2:
#                 max_stim_dur = 0.4
#                 average, initial = variable_calc('stim_dur_dm', max_stim_dur, max_stim_dur)
#                 acc = (dm_df['first_correct_bool'].mean() + ds_df['first_correct_bool'].mean())/2
#                 last3_stim_dur = df_last3.loc[df_last3['trial'] == 10]['stim_dur_dm'].median()
#                 acc_up = 0.55
#                 acc_down = 0.4
#                 change = 0.05
#             elif substage ==3:
#                 max_stim_dur = 0.35
#                 average, initial = variable_calc('stim_dur_dl', max_stim_dur, max_stim_dur)
#                 acc = (dl_df['first_correct_bool'].mean() + dm_df['first_correct_bool'].mean()) / 2
#                 last3_stim_dur = df_last3.loc[df_last3['trial'] == 10]['stim_dur_dl'].median()
#                 acc_up = 0.5
#                 acc_down = 0.35
#                 change = 0.025

#             if task == 'StageTraining_10B_V3':
#                 max_stim_dur = 0.65
#                 average, initial = variable_calc('stim_dur_ds', max_stim_dur, max_stim_dur)
#                 acc = ds_df['first_correct_bool'].mean()
#                 last3_stim_dur = df_last3.loc[df_last3['trial'] == 10]['stim_dur_ds'].median()
#                 acc_up = 0.80
#                 acc_down = 0.60
#                 change = 0.075

#             # Good accuracy -> shorten stim_dur
#             if acc > acc_up and n_trials>55:
#                 if initial >= change:
#                     stim_dur = initial - change
#                 else:
#                     stim_dur = 0
#                     if last3_stim_dur < change and len(last5_substages)==1: # if stim_dur is the minimum for 3 sessions advance stage
#                         next_stage = True  # next substage

#             # Bad accuracy or desmotivation -> elongate stim_dur
#             else:
#                 stim_dur = initial # maintain last session value unless ...
#                 if n_trials <= 25 and n_trials_prev<= 25:       # Hard desmotivation
#                     if initial <= max_stim_dur:
#                         stim_dur = initial + change
#                     else:
#                         if last3_stim_dur >= max_stim_dur:
#                             lower_stage =True # lower substage
#                 if acc <acc_down:                               # Low specific accuracy
#                     if initial <= max_stim_dur:
#                         stim_dur = initial + change
#                 if df_last3.first_correct_bool.mean() <= 0.4:   # Low global accuracy
#                     lower_stage = True # lower substage

#             if substage == 1:  # stage 2 remain now in substage 1 ds 0
#                 stim_dur_ds = stim_dur
#                 if next_stage == True:
#                     substage += 1
#                     stim_dur_ds = 0
#                     stim_dur_dm = 0.4
#                 elif lower_stage == True:
#                     stage -=1
#                     substage = float(3)
#                     stim_dur_ds = 0.45
#             elif substage == 2:
#                 if task != 'StageTraining_10B_V3':
#                     stim_dur_dm = stim_dur
#                     if next_stage == True:
#                         substage += 1
#                         stim_dur_dm = 0
#                         stim_dur_dl = 0.35
#                     elif lower_stage == True:
#                         substage -=1
#                         stim_dur_ds = 0.45
#                         stim_dur_dm = 0
#             elif substage == 3:
#                 stim_dur_dl = stim_dur
#                 if next_stage == True:
#                     print('pass') #decide manually when to move them forward
#                     # stage += 1
#                     # substage = float(1)
#                     # stim_dur_dl = 0
#                 elif lower_stage == True:
#                     substage -=1
#                     stim_dur_dm = 0.4
#                     stim_dur_dl = 0



