"""
-*- coding: utf-8 -*-
@Time    : 05/12/2022 18:10
@Author :   KarenJ
@Note   :   This function is to generate a feasible disassembly sequence
            and its corresponding disassembly direction.
"""


import numpy as np
import random

import Fn_ProcessExcelData as Fn


'''ABBREVIATIONS: 
ds->disassembly; dir->direction; comp->comp_num.
'''


def generate_feasible_sequence(mtx_sum, mtx_itf, num_comp):
    mtx_s = mtx_sum

    '''Generate an empty sequence and direction list.'''
    sequence = np.zeros(num_comp, dtype=int)
    direction = np.zeros(num_comp, dtype=int)

    '''Find the location and direction of detachable components from interference result.'''
    [ds_dir, ds_comp] = np.array(np.nonzero(mtx_s == 0))
    # print("These components with directions(0->pos, 1->neg) are able to be diassembled: \n", [ds_comp, ds_dir])

    '''Find the number of detachable components in CAD model.'''
    num_detach_comp = len(ds_comp)
    # print("This detachable components number is: \n", num_detach_comp)

    '''Randomly(temporarily) pick a comp_num to remove it.'''
    temp = random.randint(0, num_detach_comp - 1)
    # print(f"From 0 to {num_detach_comp} detachable components, randomly pick a number: {temp} \n")

    '''Store the picked comp_num to the sequence.'''
    sequence[0] = ds_comp[temp]

    '''Check the direction-freedom of the picked comp_num.'''
    free = []
    for i in range(0, len(ds_comp)):
        if ds_comp[i] == ds_comp[temp]:
            free.append(ds_dir[i])

    '''From all the direciton-freedoms, randomly pick one as the disassembly direciton of picked comp_num and store.'''
    free_dir = free[random.randint(0, len(free) - 1)]
    # print("The picked comp_num has direction-freedom on: ", free)
    direction[0] = free_dir
    # print("The current disassembly sequence and direction is: \n", sequence, '\n', direction)
    # print("*"*88)

    for num in range(1, num_comp):
        '''Remove the information of disassembled comp_num from the summation matrix.'''

        pop_xp = np.array(mtx_itf[0][:, sequence[num-1]])
        pop_xn = np.array(mtx_itf[1][:, sequence[num-1]])
        pop_yp = np.array(mtx_itf[2][:, sequence[num-1]])
        pop_yn = np.array(mtx_itf[3][:, sequence[num-1]])
        pop_zp = np.array(mtx_itf[4][:, sequence[num-1]])
        pop_zn = np.array(mtx_itf[5][:, sequence[num-1]])
        pop_itf = np.array([pop_xp, pop_xn, pop_yp, pop_yn, pop_zp, pop_zn])
        mtx_s = np.array(mtx_s - pop_itf, dtype=object)
        mtx_s[:, sequence[num-1]] = np.nan
        # print(f"The {num} temporary interference summation matrix result is: \n", mtx_s)

        '''Find the current location and direction of detachable components from interference result.'''
        [ds_dir, ds_comp] = np.array(np.nonzero(mtx_s == 0))
        # print("These components with directions(0->pos, 1->neg) are able to be diassembled: \n", [ds_comp, ds_dir])

        '''Find the current number of detachable components in CAD model.'''
        num_detach_comp = len(ds_comp)
        # print("This detachable components number is: \n", num_detach_comp)

        '''Randomly(temporarily) pick a comp_num to remove it.'''
        temp = random.randint(0, num_detach_comp - 1)

        '''Store the picked comp_num to the sequence.'''
        sequence[num] = ds_comp[temp]

        '''Check the direction-freedom of the picked comp_num.'''
        free = []
        for i in range(0, len(ds_comp)):
            if ds_comp[i] == ds_comp[temp]:
                free.append(ds_dir[i])

        '''From all the direciton-freedoms, randomly pick one as the disassembly direciton of picked comp_num and store.'''
        free_dir = free[random.randint(0, len(free) - 1)]
        # print("The picked comp_num has direction-freedom on: ", free)
        direction[num] = free_dir
        # print("The current disassembly sequence and direction is: \n", sequence, '\n', direction)
        # print("*"*88)
    return sequence, direction


''' Function testing:
file = 'GearMotor_9parts_EDBAdata_Kaiwen.xlsx'

itf_xp = Fn.load_from_excel(file, 'InterferenceXPlus')
itf_xn = Fn.load_from_excel(file, 'InterferenceXMinus')
itf_yp = Fn.load_from_excel(file, 'InterferenceYPlus')
itf_yn = Fn.load_from_excel(file, 'InterferenceYMinus')
itf_zp = Fn.load_from_excel(file, 'InterferenceZPlus')
itf_zn = Fn.load_from_excel(file, 'InterferenceZMinus')
interference_matrix = np.array([itf_xp, itf_xn, itf_yp, itf_yn, itf_zp, itf_zn])

sum_xp = Fn.sum_by_row(itf_xp)
sum_xn = Fn.sum_by_row(itf_xn)
sum_yp = Fn.sum_by_row(itf_yp)
sum_yn = Fn.sum_by_row(itf_yn)
sum_zp = Fn.sum_by_row(itf_zp)
sum_zn = Fn.sum_by_row(itf_zn)
sum_data = np.array([sum_xp, sum_xn, sum_yp, sum_yn, sum_zp, sum_zn])

generate_feasible_sequence(sum_data, interference_matrix, num_comp=9)
'''