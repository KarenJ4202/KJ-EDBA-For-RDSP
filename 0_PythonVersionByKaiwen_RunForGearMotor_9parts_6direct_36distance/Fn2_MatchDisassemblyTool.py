"""     
-*- coding: utf-8 -*-
@Time   :   23/01/2023 19:45
@Author :   KarenJ
@Note   :   This function is to match the corresponding disassembly tools
            to the generated feasible disassembly seuqence.
"""

import numpy as np

def match_tools(sequence, tool_data, num_comp):
    data = tool_data.flatten()

    '''Generate an empty tool list.'''
    tool = np.array(np.zeros(num_comp, dtype=int))

    for i in range(0, num_comp):
        tool[i] = data[sequence[i]]
    return tool
