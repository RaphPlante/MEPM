#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

def print_table_in_console(data):
    # Constructing the DataFrame
    df = pd.DataFrame(data)
    
    # Displaying the DataFrame
    print(df)

"""# Example usage:
data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print_table_in_console(data)"""
