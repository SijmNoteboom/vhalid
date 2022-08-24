# from matplotlib.pyplot import table
from Demographics import Demographics
from Castor import Castor
from ClinicalInfo import ClinicalInfo

import pandas as pd
import numpy as np

def main():
    information = Castor()
    amount_of_patients = information.table.shape[0]
    for file in np.arange(3, 20):
        length_id = len(str(file))
        if length_id == 1:
            pt_id = int(f"11000{file}") 
        elif length_id == 2:
            pt_id = int(f"1100{file}")
        else:
            pt_id = int(f"110{file}")

        ids = np.where(information.table["Participant Id"] == int(pt_id))[0][0]

        patient = ClinicalInfo(ids, Castor())
        list_vha = list(("vha2", "vha4"))

        if pd.isna(patient.row[patient.var == "vha1_VHA1_Tijd_bloedafname_VHA"][0]):
            continue
        else:
            demograph = Demographics(ids, Castor())
            list_demo = list(["table_one"])

            patient.surg_timeline()
            # patient.get_vha1()
            patient.get_vha2()
            patient.get_vha4_3()
        if not pd.isna(patient.row[patient.var == "vha5_1_VHA5_Tijd_bloedafname_VHA"][0]):
            patient.get_vha5()
            list_vha.append("vha5")
        if not pd.isna(patient.row[patient.var == "vha6_1_VHA6_Tijd_bloedafname_VHA"][0]):
            patient.get_vha6()
            list_vha.append("vha6")
        if not pd.isna(patient.row[patient.var == "vha7_VHA7_Tijd_bloedafname_VHA"][0]):
            patient.get_vha7()
            list_vha.append("vha7")
        if not pd.isna(patient.row[patient.var == "vha8_1_VHA8_Tijd_bloedafname_VHA"][0]):
            patient.get_vha8()
            list_vha.append("vha8")
        if not pd.isna(patient.row[patient.var == "vha9_1_VHA8_Tijd_bloedafname_VHA"][0]):
            patient.get_vha9()
            list_vha.append("vha9")

        Castor._print_dataframe(patient, file + 1, list_vha)
        Castor._print_dataframe(demograph, file + 1, list_demo)

if __name__ == '__main__':
    main()
