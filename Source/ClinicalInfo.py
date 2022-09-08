from multiprocessing.sharedctypes import Value
from posixpath import pathsep
from time import strptime
from tracemalloc import start
from Castor import Castor

import pandas as pd
import numpy as np
import math

import datetime

from dataclasses import dataclass, field

from Translate import Translate

@dataclass
class ClinicalInfo(Translate): 
    ids: int
    info: pd.DataFrame

    def __post_init__(self):
        # if self.patient_number in self.info.table.index:
        #      self.row = self.info.table.iloc[self.patient_number]
        # self.var = self.row.index

        self.row = self.info.table.iloc[self.ids]
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
        start_time = datetime.datetime.strptime(self.row[var == "time_start_aorta_clamp"][0], "%H:%M")
        end_time = datetime.datetime.strptime(self.row[var == "time_end_aorta_clamp"][0], "%H:%M")
        clamp_time = (end_time - start_time).seconds / 60 
        self.surg_timeline.loc["Time on clamp (min)"] = clamp_time

        self.incision_time = np.float64(self.row[var == "time_incision"][0].replace(':', '.'))

    def _vha_parent(self, num, vha_df):
        #TODO: bij "iets" toegediend staat niet altijd ja -> veranderen: check of er iets in "dosering" / "tijd_stop" staat
        var = self.var
        try:
            time_vha = self.row[var == f"vha{num}_VHA{num}_Tijd_bloedafname_VHA"][0]
        except IndexError:
            try:
                time_vha = self.row[var == f"vha{num}_1_VHA{num}_Tijd_bloedafname_VHA"][0]
            except IndexError:
                time_vha = self.row[var == f"vha{num}_1_VHA{num}_Tijd_bloedafname_VHA_"][0]

        # when blood product are applied
        if num == 2 or num == 3 or num == 4 or num == 5 or num == 8 or num == 9:
            num = "2_2" if num == 2 else num
            num = "8_2" if num == 8 else num
            num = "9_21" if num == 9 else num

            list_products = list()

            # if self.row[var == f"vha{num}_Cellsaver_Coagulant_toegediend?"][0] in ("Ja", "ja"):
                
            if self.row[var == f"vha{num}_Cellsaver_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Cellsaver_Dosering_mL_"].isna()[0]:
                vha_df.loc["Amount of Cellsaver, administered prior to VHA (mL)"] = self.row[var == f"vha{num}_Cellsaver_Dosering_mL_"][0]

            if self.row[var == f"vha{num}_Packed_Cells_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Packed_Cells_Dosering_mL_"].isna()[0]:
                list_products.append("Packed red blood cells<br>")
                vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Packed_Cells_Tijd_stop", time_vha)
            if self.row[var == f"vha{num}_Thrombocyten_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Thrombocyten_Dosering_mL_"].isna()[0]:
                list_products.append("Thrombocytes<br>")
                try:
                    vha_df = vha_df.drop(index=["Time after coagulation therapy (min)"])
                except KeyError:
                    pass
                finally:
                    try:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Thrombocyten_Tijd_stop", time_vha)
                    except ValueError:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time           
            if self.row[var == f"vha{num}_Fresh_Frozen_Plasma_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Fresh_Frozen_Plasma_Dosering_mL_"].isna()[0]:
                list_products.append("Plasma transfusion<br>")
                try:
                    vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
                except KeyError:
                    pass
                finally:
                    try:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Fresh_Frozen_Plasma_Tijd_stop", time_vha)
                    except ValueError:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time   
            if self.row[var == f"vha{num}_Cofact_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Cofact_Dosering_mL_"].isna()[0]:
                list_products.append("(Four factor) prothrombin complex concentrate<br>")
                try:
                    vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
                except KeyError:
                    pass
                finally:
                    try:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Cofact_Tijd_stop", time_vha)
                    except ValueError:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time   
            if self.row[var == f"vha{num}_DDAVP_Minirin__Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_DDAVP_Minirin__Dosering_mL_"].isna()[0]:
                list_products.append("Desmopressin<br>")
                try:
                    vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
                except KeyError:
                    pass
                finally:
                    try:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_DDAVP_Minirin__Tijd_stop", time_vha)
                    except ValueError:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time          
            if self.row[var == f"vha{num}_Antigibrinolytics_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Antigibrinolytics_Dosering_mL_"].isna()[0]:
                list_products.append("Antigibrinolytics<br>")
                try:
                    vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
                except KeyError:
                    pass
                finally:
                    try:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Antigibrinolytics_Tijd_stop", time_vha)
                    except ValueError:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time  
            if self.row[var == f"vha{num}_Heparine_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Heparine_Dosering_mL_"].isna()[0]:
                list_products.append("Heparin<br>")
                try:
                    vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
                except KeyError:
                    pass
                finally:
                    try:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Heparine_Tijd_stop", time_vha)
                    except ValueError:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time  
            if self.row[var == f"vha{num}_Overig_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Overig_Dosering_mL_"].isna()[0]:
                list_products.append("Protamin<br>")
                try:
                    vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
                except KeyError:
                    pass
                finally:
                    try:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Overig_Tijd_stop", time_vha)
                    except ValueError:
                        vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time 
            if list_products:
                vha_df.loc["Administered products before VHA"] = "\n".join(list_products)
        return vha_df

    def _get_timeline(self, start_str: str, stop_time: np.float64) -> int:
        if not self.row[self.var == start_str][0] <= 0:
            start_time = self.row[self.var == start_str][0]
            if type(start_time) == str:
                start_time = np.float64(start_time.replace(':', '.'))
            time_to_vha = abs(datetime.timedelta(minutes=stop_time % 1 * 100, hours = np.floor(stop_time)) \
                    - datetime.timedelta(minutes=start_time % 1 * 100, hours = np.floor(start_time))).seconds / 60
            return time_to_vha
        else:
            raise ValueError

    def get_vha1(self):
        num = 1
        var = self.var
        vha1 = pd.DataFrame(columns=["Values"])
        try:
            time_vha = self.row[var == f"vha{num}_VHA{num}_Tijd_bloedafname_VHA"][0]
        except IndexError:
            try:
                time_vha = self.row[var == f"vha{num}_1_VHA{num}_Tijd_bloedafname_VHA"][0]
            except IndexError:
                time_vha = self.row[var == f"vha{num}_1_VHA{num}_Tijd_bloedafname_VHA_"][0]
        
        time_to_vha = abs(datetime.timedelta(minutes=time_vha % 1 * 100, hours = np.floor(time_vha)).seconds \
                 - datetime.timedelta(minutes=self.incision_time % 1 * 100, hours = np.floor(self.incision_time)).seconds) / 60
        num_cor = num - 1 if num == 4 else num
        num_cor = num - 6 if num >= 7 else num
        vha1.loc[f"Timespan of VHA{num_cor} since incision"] = f"{int(time_to_vha)} minutes"
        self.vha1 = vha1

    def get_vha2(self):
        num = 2
        var = self.var
        vha2 = pd.DataFrame(columns=["Values"])
        self.vha2 = self._vha_parent(num, vha2)

        if self.row[var == "tranex"][0] == "Yes":
            # vha2.loc["Time (min) of tranexamic acid administration after incision"] = self._get_timeline("tranex_time", self.incision_time)
            vha2.loc["Dosis of tranexamic acid before CPB (mg)"] = self.row[var == "tranex_dose"][0] # round(self.row[var == "tranex_dose"][0] / int(self.row[var == "weight"][0]), 1)

        if not math.isnan(self.row[var == "dose_heparin_2"]):
            if not math.isnan(self.row[var == "dose_heparin_3"]):
                hep_dosage = self.row[var == "dose_heparin"][0] + self.row[var == "dose_heparin_2"][0] + self.row[var == "dose_heparin_3"][0]
            else:
                hep_dosage = self.row[var == "dose_heparin"][0] + self.row[var == "dose_heparin_2"][0]
        else:
            hep_dosage = self.row[var == "dose_heparin"][0]

        # vha2.loc["Time (min) of heparin administration after incision"] = self._get_timeline("time_heparin", self.incision_time)
        vha2.loc["Dosis of heparin before CPB (I.U.)"] = hep_dosage # round(hep_dosage / int(self.row[var == "weight"][0]), 1)

        vha2.loc["Level of bleeding according physician at the OR"] = ClinicalInfo._translate_bleeding(
            self.row[var == "vha2_1_VHA2_Mate_van_bloeding_volgens_arts?"][0])
        if self.row[var == "8.4|Coagulanten toegediend na VHA1?"][0] == "Yes":
            # TODO: add option --> when blood products are given before VHA
            pass
    
    def get_vha3(self):
        "VHA3 has never been done, so for pragmatic purposes -> our VHA4 becomes VHA3 for the experts"
        pass

    def get_vha4_3(self):
        num = 4
        var = self.var
        vha4 = pd.DataFrame(columns=["Values"])
        vha4.loc["Level of bleeding according physician at the OR"] = ClinicalInfo._translate_bleeding(
            self.row[var == "vha4_1_VHA4_Mate_van_bloeding_volgens_arts?"][0])
        self.vha4 = self._vha_parent(num, vha4)    

    def get_vha5(self):
        num = 5
        var = self.var
        vha5 = pd.DataFrame(columns=["Values"])
        vha5.loc["Level of bleeding according physician at the OR"] = ClinicalInfo._translate_bleeding(
            self.row[var == "vha5_1_VHA5_Mate_van_bloeding_volgens_arts?"][0])
        self.vha5 = self._vha_parent(num, vha5) 

    def get_vha6(self):
        num = 6
        var = self.var
        vha6 = pd.DataFrame(columns=["Values"])
        vha6.loc["Level of bleeding according physician at the OR"] = ClinicalInfo._translate_bleeding(
            self.row[var == "vha6_1_VHA6_Mate_van_bloeding_volgens_arts?"][0])
        self.vha6 = self._vha_parent(num, vha6)      

    def get_vha7(self):
        num = 7
        var = self.var
        vha7 = pd.DataFrame(columns=["Values"])
        vha7.loc["Time of VHA at ICU"] = "2 hours after ICU arrival"
        vha7.loc["Intervention within 2 hours after ICU arrival"] = "No"
        drain_production = self.row[var == "vha7_VHA7_Drainproductie_tot_bloedafname"][0]
        if pd.isna(drain_production):
            drain_production = "Unknown"
        vha7.loc["Drain production until VHA1 (mL)"] = drain_production
        self.vha7 = self._vha_parent(num, vha7)

    def get_vha8(self):
        num = 8
        var = self.var
        vha8 = pd.DataFrame(columns=["Values"])
        vha8.loc["Drain production until VHA2 (mL)"] = self.row[var == "vha8_1_VHA8_Drain_productie_voor_bloedafname"][0] 
        self.vha8 = self._vha_parent(num, vha8)

    def get_vha9(self):
        num = 8
        var = self.var
        vha9 = pd.DataFrame(columns=["Values"])
        vha9.loc["Drain production until VHA3 (mL)"] = self.row[var == "vha9_1_VHA8_Drain_productie_voor_bloedafname"][0] 
        self.vha9 = self._vha_parent(num, vha9)

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
    patient = ClinicalInfo(4, Castor())
    patient.surg_timeline()
    patient.get_vha2()
    patient.get_vha4_3()
    patient.get_vha7()
    Castor._print_dataframe(patient.patient_number, patient.vha4)
