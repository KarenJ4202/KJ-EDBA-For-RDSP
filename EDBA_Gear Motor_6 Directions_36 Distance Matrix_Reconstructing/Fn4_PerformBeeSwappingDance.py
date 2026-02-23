"""     
-*- coding: utf-8 -*-
@Time   :   12/02/2023 17:25
@Author :   KarenJ
@Note   :   This function is to perform Bees Algorithm local search strategies:
            swap (type0), insertion(type1) and mutation(type2).
"""
import copy

import numpy as np
import random


def local_search(sequence, direction, cad_num):
    seq = copy.deepcopy(sequence)
    direct = copy.deepcopy(direction)
    num = cad_num

    def type0_swap():
        rand = np.random.randint(num, size=2)

        '''Randomly pick two positions from the input sequence.'''
        pick_position1 = rand[0]
        pick_position2 = rand[1]
        # print("pick positions: ", pick_position1, pick_position2)

        '''Locate the first position's value in the sequence and direction.'''
        temp_seq = seq[pick_position1]
        temp_direct = direct[pick_position1]

        '''Transfer values from the second location to the first one.'''
        seq[pick_position1] = seq[pick_position2]
        direct[pick_position1] = direct[pick_position2]

        '''Transfer the temperary stored values to the first locaton.'''
        seq[pick_position2] = temp_seq
        direct[pick_position2] = temp_direct

        new_sequence = seq
        new_direction = direct

        return new_sequence, new_direction

    def type1_insertion():
        rand = random.sample(range(num), 2)

        new_sequence = seq
        new_direction = direct

        if rand[0] < rand[1]:
            index_before = rand[0]
            index_after = rand[1]
        else:
            index_before = rand[1]
            index_after = rand[0]
        # print("insert position (before, after): ", index_before, index_after)

        length = index_after - index_before + 1

        temp_seq = seq[index_before: index_after + 1]
        temp_direct = direct[index_before: index_after + 1]
        # print('temp seq and direct: \n', temp_seq, temp_direct)

        insert_seq = np.append(temp_seq[-1], temp_seq[0:length-1])
        insert_direct = np.append(temp_direct[-1], temp_direct[0:length-1])
        # print('insert seq and direct: ', insert_seq, insert_direct)

        new_sequence[index_before: index_after + 1] = insert_seq
        new_direction[index_before: index_after + 1] = insert_direct

        # print('new seq and direct: \n', new_sequence, new_direction)

        return new_sequence, new_direction

    def type2_mutation():
        rand = random.sample(range(num), 1)

        new_sequence = seq
        new_direction = direct

        if direct[rand] == np.any((0, 2, 4)):
            direct[rand] += 1
        elif direct[rand] == np.any((1, 3, 5)):
            direct[rand] -= 1

        return new_sequence, new_direction

    rand_type = random.randint(0, 2)
    # rand_type = 2
    if rand_type == 0:
        # print("Swapping Strategy: ")
        [offs_sequence, offs_direction] = type0_swap()
        return offs_sequence, offs_direction

    elif rand_type == 1:
        # print("Insertion Strategy: ")
        [offs_sequence, offs_direction] = type1_insertion()
        return offs_sequence, offs_direction

    elif rand_type == 2:
        # print("Mutation Strategy: ")
        [offs_sequence, offs_direction] = type2_mutation()
        return offs_sequence, offs_direction
