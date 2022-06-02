from time import strptime
from tracemalloc import start
from Castor import Castor

import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt

from datetime import datetime

from dataclasses import dataclass, field

from Translate import Translate

@dataclass
class ClinicalInfo(Translate): 
    patient_number: int
    info: pd.DataFrame

    def __post_init__(self):
        if self.patient_number in self.info.table.index:
             self.row = self.info.table.iloc[self.patient_number]
        self.var = self.row.index
    
    def post_surgery(self):
        var = self.var
        self.post_surgery = pd.DataFrame(columns=['Value'])
        
        # pump time
        start_time = datetime.strptime(self.row[var == "time_ecc_start"][0], "%H:%M")
        end_time = datetime.strptime(self.row[var == "time_ecc_end"][0], "%H:%M")
        pump_time = (end_time - start_time).seconds / 60 
        self.surg_timeline.loc["Time on CPB (min)"] = pump_time
    
    def surg_timeline(self):
        var = self.var
        self.surg_timeline = pd.DataFrame(columns=['Value'])

        # clamp time
        start_time = datetime.strptime(self.row[var == "time_start_aorta_clamp"][0], "%H:%M")
        end_time = datetime.strptime(self.row[var == "time_end_aorta_clamp"][0], "%H:%M")
        clamp_time = (end_time - start_time).seconds / 60 
        self.surg_timeline.loc["Time on clamp (min)"] = clamp_time

        

    def _vha_parent(self, num, vha_df):
        var = self.var
        try:
            time_vha = self.row[var == f"vha{num}_VHA{num}_Tijd_bloedafname_VHA"][0]
        except IndexError:
            try:
                time_vha = self.row[var == f"vha{num}_1_VHA{num}_Tijd_bloedafname_VHA"][0]
            except IndexError:
                time_vha = self.row[var == f"vha{num}_1_VHA{num}_Tijd_bloedafname_VHA_"][0]
        vha_df.loc[f"Time VHA {num}"] = format(time_vha, '.2f')
     
        return vha_df
        
    def vha1(self):
        num = 1
        var = self.var
        vha1 = pd.DataFrame(columns=["Values"])
        
       
        # self.vha1 = self._vha_parent(num, vha1)

    def get_vha2(self):
        num = 2
        var = self.var
        vha2 = pd.DataFrame(columns=["Values"])
        self.vha2 = self._vha_parent(num, vha2)

        # before pump
        self.vha2.loc["ACT value (before tranexamic acid and heparin)"] = self.row[var == "ACT_0"][0]
        if self.row[var == "tranex"][0] == "Yes":
            vha2.loc["Time tranexamic acid administration (before CPB)"] = self.row[var == "tranex_time"][0]
            if self.row[var == "tranex_dose"][0] > 1:
                vha2.loc["Dose of tranexamic acid (mg)"] = self.row[var == "tranex_dose"][0]
            else:
                vha2.loc["Dose of tranexamic acid (mg)"] = "Unknown"
        vha2.loc["Time heparin administration (before CPB)"] = self.row[var == "time_heparin"][0]
        vha2.loc["Heparin dose (I.U.)"] = self.row[var == "dose_heparin"][0]
        if self.row[var == "Value_ACT2"][0] >= 0:
            act_value1 = self.row[var == "Value_ACT1"][0]
        else:
            act_value1 = self.row[var == "Value_ACT2"][0]
        vha2.loc["ACT value"] = act_value1

        # in case of second (and third) heparin administration
        vha2 = self.__extra_heparin(var, vha2)

        # info during clamp
        vha2 = self.__during_clamp(var, vha2)
    
    def get_vha3(self):
        vha3 = pd.DataFrame(columns=["Values"])

    def get_vha4(self):
        vha4 = pd.DataFrame(columns=["Values"])

    def __extra_heparin(self, var, vha2):
        if self.row[var == "hep2"][0] == "Yes":
            vha2.loc["Second heparin dose (I.U.) (if applicable)"] = self.row[var == "dose_heparin_2"]
            vha2.loc["ACT value"] = self.row[var == "Value_ACT3"][0]
        if self.row[var == "hep3"][0] == "Yes":
            vha2.loc["Third heparin dose (I.U.) (if applicable)"] = self.row[var == "dose_heparin_3"]
            vha2.loc["ACT value"] = self.row[var == "Value_ACT4"][0]
        return vha2  
    
    def __during_clamp(self, var, vha2):
        # clamp time
        start_time = datetime.strptime(self.row[var == "time_start_aorta_clamp"][0], "%H:%M")
        end_time = datetime.strptime(self.row[var == "time_end_aorta_clamp"][0], "%H:%M")
        clamp_time = (end_time - start_time).seconds / 60 
        self.vha2.loc["Total time of aorta clamp (min)"] = clamp_time

        # heparin/tranex during cpb
        self.vha2.loc["Heparin dose during clamp/CPB"] = self.row[var == "Hepa_pomp"][0]
        self.vha2.loc["Tranexamic acid dose during clamp/CPB"] = self.row[var == "Tranex_pomp"][0]

        self.vha2.loc["Lowest temperature during CPB"] = self.row[var == "temp_lowest"][0]


if __name__ == "__main__":
    patient = ClinicalInfo(13, Castor())
    patient.surg_timeline()
    patient.get_vha2()
    x = 3