from Castor import Castor

import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt

from dataclasses import dataclass, field

from Translate import Translate

@dataclass
class ClinicalInfo(Translate):
    patient_number: int
    info: pd.DataFrame

    def __post_init__(self):
        if self.patient_number in self.info.table.index:
             self.row = self.info.table.iloc[self.patient_number]
    
    def _vha_parent(self):
        pass

    def vha1(self):
        pass

    def vha2(self):
        pass