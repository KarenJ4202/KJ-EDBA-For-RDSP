"""     
-*- coding: utf-8 -*-
@Time   :   21/02/2023 17:15
@Author :   KarenJ
@Note   :   This function is to check the feasibility of generated sequence and direction.
            If the sequence is a feasible one, keep it;
            if no, eluminate it and jump back to main loop, re-generate.
"""

import numpy as np

import Fn_ProcessExcelData as Fn


def check_feasibility(mtx_sum, mtx_itf, sequence, direction, num_comp):
    mtx_s = np.array(mtx_sum)
    mtx_i = np.array(mtx_itf)
    i_xp = mtx_i[0]
    i_xn = mtx_i[1]
    i_yp = mtx_i[2]
    i_yn = mtx_i[3]
    i_zp = mtx_i[4]
    i_zn = mtx_i[5]

    seq = sequence
    direct = direction
    num = num_comp

    for comp in range(0, num):
        # print('Current summation matrix: \n', temp_mtx_sum)
        if mtx_s[direct[comp], seq[comp]] == 0:
            temp_comp_info = np.array([i_xp[:, seq[comp]],
                                       i_xn[:, seq[comp]],
                                       i_yp[:, seq[comp]],
                                       i_yn[:, seq[comp]],
                                       i_zp[:, seq[comp]],
                                       i_zn[:, seq[comp]]])
            # print('the selected comp_num interference info (pos, neg): \n', temp_comp_info)
            mtx_s -= temp_comp_info
            # print('after excluding current comp_num: \n', temp_mtx_sum)
            if comp == num - 1:
                feasibility = True
                return feasibility
        else:
            feasibility = False
            return feasibility


''' Function testing:
file = '/Users/karenj/Documents/Git/DisassemblyCollaboration/CAD/0_GearMotor_9parts/GearMotor_9parts_EDBAdata_Kaiwen.xlsx'

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

sequence = [3, 2, 6, 4, 1, 8, 7, 5, 0]
direction = [1, 4, 1, 5, 4, 1, 3, 4, 1]

a = check_feasibility(sum_data, interference_matrix, sequence, direction, num_comp=9)
print(a)
'''