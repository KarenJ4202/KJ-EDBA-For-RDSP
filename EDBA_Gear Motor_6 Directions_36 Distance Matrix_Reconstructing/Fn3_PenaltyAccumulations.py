"""
-*- coding: utf-8 -*-
@Time   :   05/01/2023 12:47
@Author :   KarenJ
@Note   :   This funciton is to calculate the accumulations for the fitness function.
            -- The content of accumulation:
                    delay by direction changes,
                    delay by tool changes,
                    moving distance of robot end-effector.
"""


def penalty_accumulating(penalty_direction, penalty_tool, distance_matrix, sequence, direction, tool, cad_num):
    value_penalty_direction = 0
    value_penalty_tool = 0
    value_distance = 0
    for i in range(0, cad_num - 1):
        m = i
        n = i + 1
        value_penalty_direction += accumulate_penalty(penalty_direction, direction[m], direction[n])
        value_penalty_tool += accumulate_penalty(penalty_tool, tool[m]-1, tool[n]-1)
        value_distance += accumulate_penalty(distance_matrix[direction[m]][direction[n]],
                                             sequence[m],
                                             sequence[n])

    return value_penalty_direction, value_penalty_tool, value_distance


def accumulate_penalty(mtx, a, b):
    value = mtx[a][b]
    return value
