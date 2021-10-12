import numpy as np
import pandas as pd
import csv


def open_file(filename):
    f = open(filename, "r")
    return f


def read_pd(filename):
    f = pd.read_csv(filename, header=None)
    return f


if __name__ == "__main__":
    data = '../Data/12871_2015_145_MOESM1_ESM.txt'
    text = open_file(filename=data)
    table = read_pd(filename=data)
    x = 3