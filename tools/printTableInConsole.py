#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd


def printTableInConsole(data):
    print(f"Type de data: {type(data)}")  # Debug
    print(f"Contenu de data: {data}")     # Debug
    df = pd.DataFrame([[data]], columns=["Valeur"])
    print(df)


# Test local
printTableInConsole(5.127011375811621)


"""# Example usage:
data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print_table_in_console(data)"""
