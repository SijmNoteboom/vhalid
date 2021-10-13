import numpy as np
import pandas as pd
import os


class File:
    def __init__(self, file_number):
        self.filename = file_number


def dict_patients(self, load_path):
    pass


if __name__ == "__main__":
    load_dir = '../Data'
    files = [i for i in os.listdir(load_dir) if os.path.isfile(os.path.join(load_dir, i)) and 'ESM' in i]
    patients = dict_patient(load_dir)
