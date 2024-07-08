# -*- coding: utf-8 -*-
"""
Python script to calculate Simple Moving Average (MA) from XVG file GROMACS analysis tools.

Author: Rogério Ribeiro Macêdo
"""
import sys
from pathlib import Path

try:
    import pandas as pd
    import matplotlib
    import math
except ImportError as e:
    print('[!] The required Python libraries could not be imported:', file=sys.stderr)
    print('\t{0}'.format(e))
    sys.exit(1)


def title():
    """
    Print a title of script.

    Returns
    -------
    None.

    """
    print("-".center(82, "-"))
    print(f"{'|':<1} {'Calculate Simple Moving Average (MA) from XVG files':^78} {'|':<1}")
    print(f'{"|":<1} {"":^78} {"|":>1}')
    print(f'{"|":<1} {"e.g. gmx energy -f min.edr min-energy.xvg -xvg none":<78} {"|":<1}')
    print(f'{"|":<1} {"  or gmx energy -f min.edr min-energy.xvg":<78} {"|":<1}')
    print(f'{"|":<1} {"":^78} {"|":<1}')
    print("-".center(82, "-"))
    print("")


def read_xvg(xvg_file_path):
    """
    Read the content of a xvg file.

    Parameters
    ----------
    xvg_file : string
        String witha a path to the xvg file.

    Returns
    -------
    data : zip
        an iterator of tuples.
    """
    data = []
    with open(xvg_file_path, 'r') as f_xvg:
        for line in f_xvg:
            line = line.strip()
            if line.startswith('@') or line.startswith('#'):
                continue
            elif line[0].isdigit():
                data.append(map(float, line.split()))

    data = zip(*data)

    return data


def moving_average(data, period):
    """
    Calculate a simple moving average.

    Parameters
    ----------
    data : zip
        values.
    period : int
        Period of time the will be considered.

    Returns
    -------
    data_ma : TYPE
        DESCRIPTION.

    """
    data_ma = []
    data = list(data)
    values = [0 for i in range(0, period)] + list(data[1])
    # print(values)
    start = 0
    end = period
    for step in data[0]:
        ma_calc = sum(values[start:end]) / period
        # print(f"({step}) ({values[start:end]}) ({ma_calc})")
        data_ma.append([step, ma_calc])
        start += 1
        end += 1

    return data_ma


def save_data(data):
    """
    Save file.

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    with open('moving_average.xvg', 'w') as f_ma_xvg:
        for i in data:
            print(f"{i[0]} {i[1]}\n")
            f_ma_xvg.write(f"{i[0]} {i[1]}\n")

    print(" + File 'moving_average.xvg' saved!")


def main():
    """
    Principal function.

    Returns
    -------
    None.

    """
    xvg_file_path = input("XVG file".ljust(20, '.') + ": ").strip()
    if Path(xvg_file_path).is_file() and Path(xvg_file_path).suffix == '.xvg':
        period = input("Specific a period of time".ljust(20, ".") + ": ").strip()
        if period.isdigit():
            data = read_xvg(xvg_file_path)
            period = int(period)
            data_ma = moving_average(data, period)
            save_data(data_ma)
        else:
            print(f' + Period of time ({period}) invalid.\n')
            sys.exit()
    else:
        print(f' + File not found: {xvg_file_path}\n')
        sys.exit()


if __name__ == "__main__":
    # Show title
    title()

    # Main function
    main()
