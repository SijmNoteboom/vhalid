from Castor import Castor

import pandas as pd

from dataclasses import dataclass, field

from Translate import Translate


@dataclass
class Demographics(Translate):
    patient_number: int
    info: pd.DataFrame

    def __post_init__(self):
        if self.patient_number in self.info.table.index:
             self.row = self.info.table.iloc[self.patient_number]

    def get_demographics(self):
        var = self.row.index
        self.demograph_df = pd.DataFrame(columns=[""])
        print(f"Patient ID = {repr(self.row[var == 'Record Id'][0])[-3:]}")

        list_param = ["age", "type_surg"]
        for param in list_param:
            if param == "type_surg":
                surgery = self.row[var == param][0]
                self.demograph_df.loc["Type of surgery"] = Demographics._translate_surg_type(surgery)
            elif param == "age":
                self.demograph_df.loc["Age"] = int(self.row[var == param][0])
            elif "-" in str(self.row[var == param][0]):
                self.demograph_df.loc[param] = "Unknown"
            else:
                self.demograph_df.loc[param] = self.row[var == param][0]

    def get_medication(self):
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
        
        overview_meds = pd.DataFrame(columns=[""])
        for med in meds_patient.index:
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
            overview_meds.loc["Current medication:"] = med_type.replace('_', ' ')
        overview_meds.loc["Stop medication, prior to surgery (hrs):"] = self.row["Stop_Thuis_Medicatie"]
        self.medication = overview_meds

    def __complete_med_name(name_med) -> str:
        if name_med == "antihyper_med":
            complete_name = "Other antihypertensive agents"
        elif name_med == "anticoag_med":
            complete_name = "Other anticoagulants"
        elif name_med == "cholest_med":
            complete_name = "Other cholesterol-lowering agents"
        return complete_name

    def get_history(self):
        id_reuma_collagen = self.row.index.get_loc("vg_reuma")
        id_coagulopathy = self.row.index.get_loc("vg_coagul")

        overview_hist = pd.DataFrame(columns=[""])
        if self.row[id_reuma_collagen] == "Yes":
            overview_hist.loc["Medical history (coagulation related)"] = "Rheumatoid arthritis or collagen vascular disease"

        if self.row[id_coagulopathy] == "Yes":
            overview_hist.loc["Medical history (coagulation related)"] = "Congenital coagulopathy"
        self.history = overview_hist


if __name__ == "__main__":
    patient = Demographics(14, Castor())
    patient.get_history()
    patient.get_medication()
    x = 3
