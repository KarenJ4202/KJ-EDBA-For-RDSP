"""     
-*- coding: utf-8 -*-
@Time   :   20/02/2026 12:20
@Author :   KarenJ
@Note   :   Read input data from excel file.
"""


import pandas as pd
import numpy as np

AXES = ["X", "Y", "Z"]
SIGNS = ["PLUS", "MINUS"]


# def load_sheet(path, sheet_name):
#     return pd.read_excel(path, sheet_name=sheet_name).to_numpy()


def load_all_sheets(path, as_array=True):
    sheets = pd.read_excel(path, sheet_name=None, header=None)

    if as_array:
        return {name: df.to_numpy() for name, df in sheets.items()}
    else:
        return sheets


def load_distance(data, n=6):
    return np.stack([
        np.stack([data[f"Distance{i}{j}"] for j in range(n)], axis=0)
        for i in range(n)
    ], axis=0)


def assemble_interference(data, axes=AXES, signs=SIGNS):
    interference_matrix = np.stack(
        [data[f"Interference{axis}{sign}"]
         for axis in axes
         for sign in signs],
        axis=0
    )  # shape: (6, 9, 9)

    sum_interference_matrix = interference_matrix.sum(axis=2)  # 按行求和 → (6, 9)

    return interference_matrix, sum_interference_matrix

