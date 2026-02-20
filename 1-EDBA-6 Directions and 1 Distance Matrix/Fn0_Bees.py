"""     
-*- coding: utf-8 -*-
@Time   :   17/01/2023 19:59
@Author :   KarenJ
@Note   :   This function is to create (scout-bees with empty information slots.
"""

import Fn2_MatchDisassemblyTool as Fn2
import Fn3_Accumulations as Fn3
import Fn4_PerformBeeSwappingDance as Fn4
import Fn5_CheckFeasibility as Fn5


def generate_BA(num):
    info_dict = {}
    for i in range(0, num):
        info_value = {
            "ScoutBeeNumber": None,
            "Sequence": [],
            "Direction": [],
            "Tool": [],
            "DirectionChange": None,
            "ToolChange": None,
            "Distance": None,
            "TotalCost": -2
        }
        info_dict[i] = info_value
    return info_dict


def print_beeinfo_BA(diction):
    for key, value in diction.items():
        print(key, value)
    print('\n')


''' Sorting the inner-dictionary.
outer_dict = {
    0: {'A': [1, 2, 3], 'B': 58},
    1: {'A': [11, 22, 33], 'B': 73},
    2: {'A': [111, 222, 333], 'B': 9}
}

"""Target output：
outer_dict = {
    2: {'A': [111, 222, 333], 'B': 9}
    0: {'A': [1, 2, 3], 'B': 58},
    1: {'A': [11, 22, 33], 'B': 73},   
}
"""

res = sorted(outer_dict, key=lambda key: outer_dict[key]['B'])
print({key: outer_dict[key] for key in res})
'''