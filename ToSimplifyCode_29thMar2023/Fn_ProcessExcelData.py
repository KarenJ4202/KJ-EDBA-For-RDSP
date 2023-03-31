"""     
-*- coding: utf-8 -*-
@Time   :   23/01/2023 21:45
@Author :   KarenJ
@Note   :   This function is to process CAD data in excel file into a format of array.
"""

import numpy as np
import pandas as pd


def excel_to_array(file_path, sheet_name):
    data = np.array(pd.read_excel(file_path, index_col=None, header=None, sheet_name=sheet_name))
    return data


def sum_by_row(itf_data):
    data = np.array(np.sum(itf_data, axis=1))
    return data


# def num_cadcomps(itf_data):
#     pick = random.choice(itf_data)
#     print(pick)
#     while pick.size != 0:
#         num = pick.shape[1]
#         return num
