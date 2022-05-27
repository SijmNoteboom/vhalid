from Castor import Castor

import pandas as pd

from dataclasses import dataclass, field

from Translate import Translate

@dataclass
class InformationPatient(Translate):
    patient_number: int
    info: pd.DataFrame

    def __post_init__(self):
        if self.patient_number in self.info.table.index:
             self.row = self.info.table.iloc[self.patient_number]

    def _get_demographics(self):
        var = self.row.index
        self.demograph_df = pd.DataFrame(columns=['Value'])
        self.demograph_df.loc["id"] = repr(self.row[var == "Record Id"][0])[-3:]
        
        list_param = ["age", "height", "weight", "bmi", "bsa", "type_surg"]
        for param in list_param:
            if param == "type_surg":
                surgery = self.row[var == param][0]
                self.demograph_df.loc[param] = InformationPatient._translate_surg_type(surgery)
            else:
                self.demograph_df.loc[param] = self.row[var == param][0]
 
    def _get_medication(self):
        start_id_meds = self.row.index.get_loc("antihyper_med#Nee")
        end_id_meds = self.row.index.get_loc("3.4|Thuismedicatie: gebruikt patiënt thrombocytenaggregatieremmers?(Overig)") + 1

        all_meds = self.row[start_id_meds:end_id_meds]
        meds_patient = all_meds[all_meds == 1]

        overview_meds = pd.DataFrame(columns=['med_type'])
        for med in meds_patient.index:
            if '3.' not in med:
                med_type = med.split(sep='#')[1].split(sep='_eg')[0]
                if med_type == 'Overig':
                    med_type == InformationPatient.__complete_med_name(med.split(sep='#')[0])
                elif med_type == "Nee":
                    continue
            else:
                med_type = med.split(sep='(')[1][:-1]
                if med_type.lower() == "overig":
                    med_type == "Other thrombocyte aggregation inhibitors"
                elif med_type.lower() == "nee":
                    continue
            overview_meds = overview_meds.append({'med_type': med_type}, ignore_index=True)
        overview_meds.loc["Stop medication, prior to surgery (hrs)"] = self.row[end_id_meds]
        self.medication = overview_meds

    def __complete_med_name(name_med) -> str:
        if name_med == "antihyper_med":
            complete_name = "Other antihypertensive agents"
        elif name_med == "anticoag_med":
            complete_name = "Other anticoagulants"
        elif name_med == "cholest_med":
            complete_name = "Other cholesterol-lowering agents"
        return complete_name

    def _get_history(self):
        start_id_hist = self.row.index.get_loc("hist_cardio_dis#Blanco")
        end_id_hist = self.row.index.get_loc("hist_renal_dis#Overig") + 1

        all_hist = self.row[start_id_hist:end_id_hist]
        hist_patient = all_hist[all_hist == 1]

        overview_hist = pd.DataFrame(columns=['hist_type'])
        for hist in hist_patient.index:
            # TODO: implement this in the med history method
            if hist.split(sep='#')[1].lower() == "blanco":
                continue
            else:
                hist_type = InformationPatient._translate_med_history(hist)
                overview_hist = overview_hist.append({'hist_type': hist_type}, ignore_index=True)
        self.history = overview_hist
        # TODO: add oncological VG and coagulant VG
                    
if __name__ == "__main__":
    patient = InformationPatient(14, Castor())
    patient._get_demographics()
    patient._get_medication()
    patient._get_history()
    x = 3
