from Castor import Castor

import pandas as pd
import numpy as np

from dataclasses import dataclass, field

from Translate import Translate


@dataclass
class Demographics(Translate):
    ids: int
    info: pd.DataFrame

    def __post_init__(self):
        # if self.patient_number in self.info.table.index:
        #     ids = np.where(self.info.table["Participant Id"] == int(self.pt_id))[0][0]
        #     self.row = self.info.table.iloc[ids]
        self.row = self.info.table.iloc[self.ids]
        self.var = self.row.index
        self.table_one = pd.concat((self.get_demographics(), self.get_history(), self.get_medication()))

    def get_demographics(self) -> pd.DataFrame:
        var = self.row.index
        self.demograph_df = pd.DataFrame(columns=["Values"])
        print(f"Patient ID = {repr(self.row[var == 'Participant Id'][0])[-3:]}")

        list_param = ["age", "type_surg", "weight", "height"]
        for param in list_param:
            if param == "type_surg":
                surgery = self.row[var == param][0]
                self.demograph_df.loc["Type of surgery"] = Demographics._translate_surg_type(surgery)
            elif param == "age":
                self.demograph_df.loc["Age (yrs)"] = int(self.row[var == param][0])
            elif param == "weight":
                self.demograph_df.loc["Weight (kg)"] = self.row[var == param][0]
            elif param == "height":
                self.demograph_df.loc["Height (cm)"] = self.row[var == param][0]
            elif "-" in str(self.row[var == param][0]):
                self.demograph_df.loc[param] = "Unknown"
            else:
                self.demograph_df.loc[param] = self.row[var == param][0]
        return self.demograph_df

    def get_medication(self) -> pd.DataFrame:
        coag_meds = pd.Series([])
        thrombo_meds = pd.Series([])
        if self.row["anticoag_med#Nee"] == 0:
            start_id_coag_meds = self.row.index.get_loc("anticoag_med#Platelet_inhibitors_eg_acetylsalicylic_acid_clopidogrel_ticagrelor__persantin")
            end_id_coag_meds = self.row.index.get_loc("anticoag_med#Overig") + 1
            coag_meds = self.row[start_id_coag_meds:end_id_coag_meds]
    
        if self.row["3.4|Thuismedicatie: gebruikt patiënt thrombocytenaggregatieremmers?(Nee)"] == 0:
            start_id_thrombo_meds = self.row.index.get_loc("3.4|Thuismedicatie: gebruikt patiënt thrombocytenaggregatieremmers?(Nee)")
            end_id_thrombo_meds = self.row.index.get_loc("3.4|Thuismedicatie: gebruikt patiënt thrombocytenaggregatieremmers?(Overig)")
            thrombo_meds = self.row[start_id_thrombo_meds: end_id_thrombo_meds]

        all_meds = pd.concat((coag_meds, thrombo_meds))

        meds_patient = all_meds[all_meds == 1]
        
        overview_meds = pd.DataFrame(columns=["Values"])
        for nr, med in enumerate(meds_patient.index):
            if '3.' not in med:
                med_type = med.split(sep='#')[1].split(sep='_eg')[0]
                if med_type == 'Overig':
                    med_type == Demographics.__complete_med_name(med.split(sep='#')[0])
                elif med_type == "Nee":
                    continue    
            else:
                med_type = med.split(sep='(')[1][:-1]
                if med_type.lower() == "overig":
                    med_type == "Other thrombocyten aggregation inhibitors"
                elif med_type.lower() == "nee":
                    continue
                overview_meds.loc[f"Current medication {nr}:"] = Demographics._translate_meds(med_type) 
            med_type = med_type.replace('_', ' ')
        
        if not overview_meds.empty:
            overview_meds.loc["Stop medication, prior to surgery (hrs):"] = self.row["Stop_Thuis_Medicatie"]
        self.medication = overview_meds
        return overview_meds

    def __complete_med_name(name_med) -> str:
        if name_med == "antihyper_med":
            complete_name = "Other antihypertensive agents"
        elif name_med == "anticoag_med":
            complete_name = "Other anticoagulants"
        elif name_med == "cholest_med":
            complete_name = "Other cholesterol-lowering agents"
        return complete_name

    def get_history(self) -> pd.DataFrame:
        id_reuma_collagen = self.row.index.get_loc("vg_reuma")
        id_coagulopathy = self.row.index.get_loc("vg_coagul")

        overview_hist = pd.DataFrame(columns=["Values"])
        if self.row[id_reuma_collagen] == "Yes":
            overview_hist.loc["Medical history (coagulation related)"] = "Rheumatoid arthritis or collagen vascular disease"

        if self.row[id_coagulopathy] == "Yes":
            overview_hist.loc["Medical history (coagulation related)"] = "Congenital coagulopathy"
        self.history = overview_hist
        return overview_hist


if __name__ == "__main__":
    patient = Demographics(16, Castor())
    Castor._print_dataframe(patient.patient_number, patient.table_one)
    x = 3
