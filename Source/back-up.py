# ClinicalInfo.py

   # back-up voor _vha_parent() --> new "def" places all blood products in one dataframe cell, this old provides new cell for all blood products 


    # def _vha_parent(self, num, vha_df):
    #     #TODO: bij "iets" toegediend staat niet altijd ja -> veranderen: check of er iets in "dosering" / "tijd_stop" staat
    #     var = self.var
    #     try:
    #         time_vha = self.row[var == f"vha{num}_VHA{num}_Tijd_bloedafname_VHA"][0]
    #     except IndexError:
    #         try:
    #             time_vha = self.row[var == f"vha{num}_1_VHA{num}_Tijd_bloedafname_VHA"][0]
    #         except IndexError:
    #             time_vha = self.row[var == f"vha{num}_1_VHA{num}_Tijd_bloedafname_VHA_"][0]

    #     # when blood product are applied
    #     if num == 2 or num == 3 or num == 4 or num == 5 or num == 8 or num == 9:
    #         num = "2_2" if num == 2 else num
    #         num = "8_2" if num == 8 else num
    #         num = "9_21" if num == 9 else num

    #         # if self.row[var == f"vha{num}_Cellsaver_Coagulant_toegediend?"][0] in ("Ja", "ja"):
                
    #         if self.row[var == f"vha{num}_Cellsaver_Coagulant_toegediend?"][0] in ("Ja", "ja") or not self.row[var == f"vha{num}_Cellsaver_Dosering_mL_"].isna()[0]:
    #             vha_df.loc["Amount of Cellsaver, administered prior to VHA"] = self.row[var == f"vha{num}_Cellsaver_Dosering_mL_"][0]

    #         if self.row[var == f"vha{num}_Packed_Cells_Coagulant_toegediend?"][0] in ("Ja", "ja"):
    #             vha_df.loc["Packed red blood cells administered before VHA?"] = "Yes"
    #             vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Packed_Cells_Tijd_stop", time_vha)
    #         if self.row[var == f"vha{num}_Thrombocyten_Coagulant_toegediend?"][0] in ("Ja", "ja"):
    #             vha_df.loc["Thrombocytes administered before VHA?"] = "Yes"
    #             try:
    #                 vha_df = vha_df.drop(index=["Time after coagulation therapy (min)"])
    #             except KeyError:
    #                 pass
    #             finally:
    #                 try:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Thrombocyten_Tijd_stop", time_vha)
    #                 except ValueError:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time           
    #         if self.row[var == f"vha{num}_Fresh_Frozen_Plasma_Coagulant_toegediend?"][0] in ("Ja", "ja"):
    #             vha_df.loc["Plasma transfusion before VHA?"] = "Yes"
    #             try:
    #                 vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
    #             except KeyError:
    #                 pass
    #             finally:
    #                 try:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Fresh_Frozen_Plasma_Tijd_stop", time_vha)
    #                 except ValueError:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time   
    #         if self.row[var == f"vha{num}_Cofact_Coagulant_toegediend?"][0] in ("Ja", "ja"):
    #             vha_df.loc["(Four factor) prothrombin complex concentrate administered before VHA?"] = "Yes"
    #             try:
    #                 vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
    #             except KeyError:
    #                 pass
    #             finally:
    #                 try:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Cofact_Tijd_stop", time_vha)
    #                 except ValueError:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time   
    #         if self.row[var == f"vha{num}_DDAVP_Minirin__Coagulant_toegediend?"][0] in ("Ja", "ja"):
    #             vha_df.loc["Desmopressin administered before VHA?"] = "Yes"
    #             try:
    #                 vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
    #             except KeyError:
    #                 pass
    #             finally:
    #                 try:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_DDAVP_Minirin__Tijd_stop", time_vha)
    #                 except ValueError:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time          
    #         if self.row[var == f"vha{num}_Antigibrinolytics_Coagulant_toegediend?"][0] in ("Ja", "ja"):
    #             vha_df.loc["Antigibrinolytics administered before VHA?"] = "Yes"
    #             try:
    #                 vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
    #             except KeyError:
    #                 pass
    #             finally:
    #                 try:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Antigibrinolytics_Tijd_stop", time_vha)
    #                 except ValueError:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time  
    #         if self.row[var == f"vha{num}_Heparine_Coagulant_toegediend?"][0] in ("Ja", "ja"):
    #             vha_df.loc["Heparin administered before VHA?"] = "Yes"
    #             try:
    #                 vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
    #             except KeyError:
    #                 pass
    #             finally:
    #                 try:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Heparine_Tijd_stop", time_vha)
    #                 except ValueError:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time  
    #         if self.row[var == f"vha{num}_Overig_Coagulant_toegediend?"][0] in ("Ja", "ja"):
    #             vha_df.loc["Protamin administered before VHA?"] = "Yes"
    #             try:
    #                 vha_df = vha_df.drop(index=["Time of VHA after coagulation therapy (min)"])
    #             except KeyError:
    #                 pass
    #             finally:
    #                 try:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time = self._get_timeline(f"vha{num}_Overig_Tijd_stop", time_vha)
    #                 except ValueError:
    #                     vha_df.loc["Time of VHA after coagulation therapy (min)"] = previous_time  
    #     return vha_df
