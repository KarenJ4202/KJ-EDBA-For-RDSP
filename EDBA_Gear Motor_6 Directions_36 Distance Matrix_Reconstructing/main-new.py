"""
-*- coding: utf-8 -*-
@Time   :   10/12/2022 21:42
@Author :   KarenJ
@Note   :   The Fitness function: an estimated disassemlby time.
            -- The estimated time include:
                    disassembly basic time,
                    robot end-effector's travel time,
                    tool change time,
                    direction change time.

            The Optimization algorithm: Bees Algorithm.
            -- Some options of parameters combination:
                (ScoutBee-SelectedSite-EliteSite-SelectedBee-EliteBee-MaxIteration)
                20-5-3-7-9-300, 22Mar2023;
                30-5-2-5-10-300, 22Mar2023;
                80-4-1-1-2-800, 22Mar2023;
                20-4-1-1-2-300, 25Mar2023.
"""
import numpy as np
import copy
import matplotlib.pyplot as plt
import time

import io_excel

import Fn0_Bees as Fn0
import Fn1_GenerateFeasibleSequence as Fn1
import Fn2_MatchDisassemblyTool as Fn2
import Fn3_PenaltyAccumulations as Fn3
import Fn4_PerformBeeSwappingDance as Fn4
import Fn5_CheckFeasibility as Fn5


'''
ABBREVIATIONS: 
itf->interference.
seq->sequence.
direct->direction.
offs->offspring.

EDBA FULL SITES:
Selected Sites(Eite sites + Non-elited sites) + Non-selected sites
'''

'''Time module: Start the program timer.'''
program_time_start = time.perf_counter()

'''**************************************'''
'''Load the CAD data from the excel file.'''
'''**************************************'''

# Load Disassembly information of the Model from the excel file.
file = 'DisassemblyData-GearMotor.xlsx'
data = io_excel.load_all_sheets(file)

basictimes = data["DisassemblyBasictimes"]
tools = data["DisassemblyTools"]
direction_penalties = data["DirectionChangePenalties"]
tool_penalties = data["ToolChangePenalties"]

# dsp_distance_nn
distance_matrix = io_excel.load_distance(data, n=6)

# itf_data, sum_data
interference_matrix, sum_interference_matrix = io_excel.assemble_interference(data)

# Count comp_num number of this model
comp_num = sum_interference_matrix.shape[1]

# Calculate the total disassembly basic time of the EoL product.
basictime = basictimes.sum()

# Specify a speed of robot end-effector.'''
robot_speed = 12

# Specify a time scale when calculating direction canges.
time_scale = 2

# Time module: Start the Algorithm timer.
algo_start_time = time.perf_counter()

# A list to hold the best TotalCost values.
ba_max_iter = 100
ba_best_time = np.zeros(ba_max_iter)

'''**********************************'''
'''Specify Bees Algorithm parameters.'''
'''**********************************'''
ba_scout_bees = 5
ba_selected_site = 4
ba_elite_site = 1
ba_selected_bees = 1
ba_elite_bees = 2

'''Prepare the bees.'''
ba_bees = Fn0.generate_BA(ba_scout_bees)
# print('This are the bees with empty information:')
# Fn0.print_beeinfo_BA(ba_bees)

'''*******************************'''
'''Initialize scout-bees for EDBA.'''
'''*******************************'''
for scout_bee in range(0, ba_scout_bees):
    [sequence, direction] = Fn1.generate_feasible_sequence(sum_interference_matrix, interference_matrix, comp_num)
    tool = Fn2.match_tools(sequence, tools, comp_num)
    [directionchange, toolchange, distance] = Fn3.penalty_accumulating(direction_penalties,
                                                                       tool_penalties,
                                                                       distance_matrix,
                                                                       sequence, direction, tool, comp_num)
    totalcost = basictime + distance / robot_speed + toolchange + directionchange * time_scale

    ba_bees[scout_bee]['ScoutBeeNumber'] = scout_bee
    ba_bees[scout_bee]['Sequence'] = sequence
    ba_bees[scout_bee]['Direction'] = direction
    ba_bees[scout_bee]['Tool'] = tool
    ba_bees[scout_bee]['DirectionChange'] = directionchange
    ba_bees[scout_bee]['ToolChange'] = toolchange
    ba_bees[scout_bee]['Distance'] = distance
    ba_bees[scout_bee]['TotalCost'] = totalcost

    '''Emunerately print content in the Scout bees.'''
    Fn0.print_beeinfo_BA(ba_bees[scout_bee])


'''*************************************************'''
'''Ascending sort scout-bees by TotalCost as a list.'''
'''*************************************************'''
sorted_babees = sorted(ba_bees, key=lambda key: ba_bees[key]['TotalCost'])
# print(sorted_babees)

'''Storing sorted information back to ba_bees as a dictionary.'''
ba_bees = {key: ba_bees[key] for key in sorted_babees}
print("Ascending result by order of {ScoutBeeNumber: TotalCost, }:")
print({key: ba_bees[key]['TotalCost'] for key in sorted_babees}, '\n')

'''******************************'''
'''Start the main EDBA algorithm.'''
'''******************************'''
for it in range(0, ba_max_iter):
    '''To each of the Selected(Elite) Sites, '''
    for elitesite in range(0, ba_elite_site):
        # print("Elite Site No.", elitesite)

        '''Locate the number of bee as the search site.'''
        num_elitesite = sorted_babees[elitesite]

        '''Find the corresponding betterbee of the search site.'''
        elite_betterbee = copy.deepcopy(ba_bees[num_elitesite])
        # print('Current best bee: \n', elite_betterbee, '\n')

        '''To each of the elite-bees in the current site.'''
        for elitebee in range(0, ba_elite_bees):
            # print("Elite bee No.", elitebee)

            '''Create a babybee to challenge the betterbee.'''
            babybee = Fn0.generate_BA(1)
            # print('A challenging better bee(empty): \n', babybee, '\n')

            '''Perform local search strategy to the babybee: swapping, inserting, (mutation).'''
            [babybee_seq, babybee_direct] = Fn4.local_search(copy.deepcopy(elite_betterbee['Sequence']),
                                                             copy.deepcopy(elite_betterbee['Direction']),
                                                             comp_num)
            # print('This babybee seq and direct: ', babybee_seq, babybee_direct)

            '''Check the feasibility of this babybee.'''
            babybee_feasibility = Fn5.check_feasibility(sum_interference_matrix, interference_matrix, babybee_seq, babybee_direct, comp_num)
            # print('Babybee feasibility: ', babybee_feasibility, '\n')

            '''Keep generating babybees until a feasible solution is found.'''
            while babybee_feasibility is False:
                [babybee_seq, babybee_direct] = Fn4.local_search(copy.deepcopy(elite_betterbee['Sequence']),
                                                                 copy.deepcopy(elite_betterbee['Direction']),
                                                                 comp_num)
                babybee_feasibility = Fn5.check_feasibility(sum_interference_matrix, interference_matrix, babybee_seq, babybee_direct, comp_num)
            # print('Babybee feasibility: ', babybee_feasibility, '\n')

            '''Generate the following information of this babybee.'''
            babybee_tool = Fn2.match_tools(babybee_seq, tools, comp_num)
            [babybee_directionchange,
             babybee_toolchange,
             babybee_distance] = Fn3.penalty_accumulating(direction_penalties,
                                                          tool_penalties,
                                                          distance_matrix,
                                                          babybee_seq,
                                                          babybee_direct,
                                                          babybee_tool,
                                                          comp_num)
            babybee_totalcost = basictime + babybee_distance / robot_speed \
                                + babybee_toolchange + babybee_directionchange * time_scale

            babybee[0]['Sequence'] = babybee_seq
            babybee[0]['Direction'] = babybee_direct
            babybee[0]['Tool'] = babybee_tool
            babybee[0]['DirectionChange'] = babybee_directionchange
            babybee[0]['ToolChange'] = babybee_toolchange
            babybee[0]['Distance'] = babybee_distance
            babybee[0]['TotalCost'] = babybee_totalcost

            if babybee_totalcost < elite_betterbee['TotalCost']:
                babybee[0]['ScoutBeeNumber'] = elite_betterbee['ScoutBeeNumber']
                elite_betterbee = copy.deepcopy(babybee[0])
            else:
                pass

            # print('babybee info: \n', babybee[0])
            # print('elite_betterbee info: \n', elite_betterbee)

        if elite_betterbee['TotalCost'] < ba_bees[num_elitesite]['TotalCost']:
            elite_betterbee['ScoutBeeNumber'] = ba_bees[num_elitesite]['ScoutBeeNumber']
            ba_bees[num_elitesite] = copy.deepcopy(elite_betterbee)
        else:
            pass

        # print(f'For site {elitesite}: ', ba_bees[num_elitesite])

    '''To each of the Selected(Non-elite) Sites,'''
    for selectedsite in range(ba_elite_site, ba_selected_site):
        # print('Selected(Non-elite) Site No.', selectedsite)

        '''Locate the number of bee as the search site.'''
        num_selectedsite = sorted_babees[selectedsite]

        '''Find the corresponding betterbee of the search site.'''
        selected_betterbee = copy.deepcopy(ba_bees[num_selectedsite])
        # print('Current best bee: \n', selected_betterbee, '\n')

        '''To each of the selected-bees in the current site.'''
        for selectedbee in range(0, ba_selected_bees):
            # print("Selected bee No.", selectedbee)

            '''Again, Create a babybee to challenge the betterbee.'''
            babybee = Fn0.generate_BA(1)
            # print('A challenging better bee(empty): \n', babybee, '\n')

            '''Perform local search strategy to the babybee: swapping, inserting, (mutation).'''
            [babybee_seq, babybee_direct] = Fn4.local_search(copy.deepcopy(selected_betterbee['Sequence']),
                                                             copy.deepcopy(selected_betterbee['Direction']),
                                                             comp_num)
            # print('This babybee seq and direct: ', babybee_seq, babybee_direct)

            '''Check the feasibility of this babybee.'''
            babybee_feasibility = Fn5.check_feasibility(sum_interference_matrix, interference_matrix, babybee_seq, babybee_direct, comp_num)
            # print('Babybee feasibility: ', babybee_feasibility, '\n')

            '''Keep generating babybees until a feasible solution is found.'''
            while babybee_feasibility is False:
                [babybee_seq, babybee_direct] = Fn4.local_search(copy.deepcopy(selected_betterbee['Sequence']),
                                                                 copy.deepcopy(selected_betterbee['Direction']),
                                                                 comp_num)
                babybee_feasibility = Fn5.check_feasibility(sum_interference_matrix, interference_matrix, babybee_seq, babybee_direct, comp_num)
            # print('Babybee feasibility: ', babybee_feasibility, '\n')

            '''Generate the following information of this babybee.'''
            babybee_tool = Fn2.match_tools(babybee_seq, tools, comp_num)
            [babybee_directionchange,
             babybee_toolchange,
             babybee_distance] = Fn3.penalty_accumulating(direction_penalties,
                                                          tool_penalties,
                                                          distance_matrix,
                                                          babybee_seq,
                                                          babybee_direct,
                                                          babybee_tool,
                                                          comp_num)
            babybee_totalcost = basictime + babybee_distance / robot_speed \
                                + babybee_toolchange + babybee_directionchange * time_scale

            babybee[0]['Sequence'] = babybee_seq
            babybee[0]['Direction'] = babybee_direct
            babybee[0]['Tool'] = babybee_tool
            babybee[0]['DirectionChange'] = babybee_directionchange
            babybee[0]['ToolChange'] = babybee_toolchange
            babybee[0]['Distance'] = babybee_distance
            babybee[0]['TotalCost'] = babybee_totalcost

            if babybee_totalcost < selected_betterbee['TotalCost']:
                babybee[0]['ScoutBeeNumber'] = selected_betterbee['ScoutBeeNumber']
                selected_betterbee = copy.deepcopy(babybee[0])
            else:
                pass

            # print('babybee info: \n', babybee[0])
            # print('selected_betterbee info: \n', selected_betterbee)

        if selected_betterbee['TotalCost'] < ba_bees[num_selectedsite]['TotalCost']:
            ba_bees[num_selectedsite]['Sequence'] = selected_betterbee['Sequence']
            ba_bees[num_selectedsite]['Direction'] = selected_betterbee['Direction']
            ba_bees[num_selectedsite]['Tool'] = selected_betterbee['Tool']
            ba_bees[num_selectedsite]['DirectionChange'] = selected_betterbee['DirectionChange']
            ba_bees[num_selectedsite]['ToolChange'] = selected_betterbee['ToolChange']
            ba_bees[num_selectedsite]['Distance'] = selected_betterbee['Distance']
            ba_bees[num_selectedsite]['TotalCost'] = selected_betterbee['TotalCost']

        # print(f'For site {selectedsite}: ', ba_bees[num_selectedsite])

    '''To each of the Non-selected Sites, assigne one bee to one site.'''
    for normalsite in range(ba_selected_site, ba_scout_bees):
        # print('Non-selected Site No.', normalsite)

        '''Locate the number of bee as the search site.'''
        num_normalsite = sorted_babees[normalsite]

        '''Create a babybee to store information.'''
        babybee = Fn0.generate_BA(1)
        # print('A challenging better bee(empty): \n', babybee, '\n')

        [babybee_seq, babybee_direct] = Fn1.generate_feasible_sequence(sum_interference_matrix, interference_matrix, comp_num)
        babybee_tool = Fn2.match_tools(babybee_seq, tools, comp_num)
        [babybee_directionchange,
         babybee_toolchange,
         babybee_distance] = Fn3.penalty_accumulating(direction_penalties,
                                                      tool_penalties,
                                                      distance_matrix,
                                                      babybee_seq,
                                                      babybee_direct,
                                                      babybee_tool,
                                                      comp_num)
        babybee_totalcost = babybee_distance / robot_speed + babybee_toolchange + babybee_directionchange * time_scale

        ba_bees[num_normalsite]['ScoutBeeNumber'] = num_normalsite
        ba_bees[num_normalsite]['Sequence'] = babybee_seq
        ba_bees[num_normalsite]['Direction'] = babybee_direct
        ba_bees[num_normalsite]['Tool'] = babybee_tool
        ba_bees[num_normalsite]['DirectionChange'] = babybee_directionchange
        ba_bees[num_normalsite]['ToolChange'] = babybee_toolchange
        ba_bees[num_normalsite]['Distance'] = babybee_distance
        ba_bees[num_normalsite]['TotalCost'] = babybee_totalcost

        # print(f'For site {normalsite}: ', ba_bees[num_normalsite])

    '''Again, Ascending sort scout-bees by TotalCost as a list.'''
    sorted_babees = sorted(ba_bees, key=lambda key: ba_bees[key]['TotalCost'])
    # print(sorted_babees)

    '''Storing sorted information back to ba_bees as a dictionary.'''
    ba_bees = {key: ba_bees[key] for key in sorted_babees}
    print("Ascending result by order of {ScoutBeeNumber: TotalCost, }:")
    print({key: ba_bees[key]['TotalCost'] for key in sorted_babees})

    '''Storing the best TotalCost of each iteration.'''
    ba_thebestbee = copy.deepcopy(ba_bees[sorted_babees[0]])
    print(f'The best bee in iteration {it} is: ', ba_thebestbee)

    ba_best_time_iter = ba_thebestbee['TotalCost']
    print(f'The best TotalCost in iteration {it} is: ', ba_best_time_iter, '\n')
    ba_best_time[it] = ba_best_time_iter

'''Time module: End the timer.'''
end_time = time.perf_counter()

'''Time module: Calculate the running time'''
program_running_time = end_time - program_time_start
algo_running_time = end_time - algo_start_time

'''Time module: Print the running time in seconds'''
print(f"Program running time: {program_running_time:.4f} seconds")
print(f"Algorithm running time: {algo_running_time:.4f} seconds")

'''Draw result figures.'''
x = range(0, ba_max_iter)
y = ba_best_time
plt.xlabel('Iteration')
plt.ylabel('The Best TotalCost')
plt.title('EDBA_Python_GearMotor9parts_Excution24.16' + '\n' +
          f'Parameter: {ba_scout_bees, ba_selected_site, ba_elite_site, ba_selected_bees, ba_elite_bees, ba_max_iter}')

fig = plt.plot(x, y)
plt.grid(True, alpha=0.5, linestyle='dotted')
plt.show()

exit()
