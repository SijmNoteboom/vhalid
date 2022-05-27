from dataclasses import dataclass

@dataclass
class Translate:

    def _translate_surg_type(surg_type: str) -> str:
        surg_translate = {"CABG": "Coronary Artery Bypass Grafting (CABG)",
                          "AVR (aortaklepvervanging)": "Aortic Valve Replacement",
                          "AVP (aortaklepplastiek)": "Aortic Valve Repair",
                          "MVR (mitraalklepvervanging)": "Mitral Valve Replacement",
                          "MVP (mitraalklepplastiek)": "Mitral Valve Repair",
                          "TVR (tricuspidaalklepvervanging)": "Tricuspid Valve Replacement",
                          "TVP (mitraalklepplastiek)": "Tricuspid Valve Repair",
                          "Klepbesparende ascendensvervanging": "Valve-Sparing Root Replacement (VSRR)",
                          "Klep-en ascendensvervanging (Bentall procedure)": "Bentall procedure",
                          "Ascendens-en boogvervanging (Elephant trunk)": "Elephant trunk procedure",
                          "PEARS": "Personalized External Aortic Root Support (PEARS)",
                          "Mini-MVP": "Mini mitral valve repair",
                          "Myxoomresectie": "Myxoma Resection",
                          "Myextomie septum": "Septal Myectomy",
                          "ASD-sluiting": "Atrial septal defect closure",
                          "VSD-sluiting": "Ventricular septal defect closure"}
        return surg_translate[surg_type]

    def _translate_med_history(hist_type: str) -> str:
        """
        hist_type consists of general/abstract history and a more specific type.
        First split into the types, then parse per specific type in other method.
        """
        
        abs_history, spec_history = hist_type.split(sep='#')

        # In case of overig
        if spec_history.lower() == "overig":
            hist = Translate.__translate_hist_other(abs_history)
        else:
            if abs_history == "hist_cardio_dis":
                hist = Translate.__translate_cardiovascular_hist(spec_history)
            elif abs_history == "hist_pulm_dis":
                hist = Translate.__translate_pulmonary_hist(spec_history)
            elif abs_history == "hist_gastroint":
                hist = Translate.__translate_gastorintestinal_hist(spec_history)
            elif abs_history == "hist_neurol":
                hist = Translate.__translate_neurological_hist(spec_history)
            elif abs_history == "hist_metabol_dis":
                hist = Translate.__translate_metabolic_hist(spec_history)
            elif abs_history == "hist_renal_dis":
                hist = Translate.__translate_renal_hist(spec_history)
        return hist
    
    def __translate_cardiovascular_hist(hist_type: str) -> str:
        hist_cardio = {"Hypertensie": "Hypertension", "Coronairlijden": "Coronary disease", 
                       "Decompensatio_cordi": "Cordial decompensation", "Atriumfibrilleren": "Atrial fibrillation", 
                       "PacemakerICD": "Pacemaker or ICD", "Open_AAA__repair": "Abdominal Aortic Aneurysm Repair (AAA)",
                       "TEVAR": "Thoracic Endovascular Aneurysm Repair (TEVAR)", "CABG": "Coronary Artery Bypass Grafting (CABG)",
                       "klepvervanging": "Valve replacement", "BentallDavid_procedure": "Bentall/David procedure"}                 
        return hist_cardio[hist_type]
    
    def __translate_pulmonary_hist(hist_type: str) -> str:
        hist_pulm = {"Astma": "Asthma", "COPD": "COPD", "Longembolie": "Pulmonary embolism"}
        return hist_pulm[hist_type]

    def __translate_gastorintestinal_hist(hist_type: str) -> str:   
            hist_GI = {"Peptisch_ulcus": "Peptic ulcer", "GIbloeding": "Gastrointestinal bleeding",
                       "IBD_Crohncolitis_ulcerose": "Inflammatory bowel disease (Crohn/Colitis ulcerosa)",
                       "Leverziekte_bijv_hepatitis_cirrose_NAFLD": "Liver disease"}
            return hist_GI[hist_type]
    

    def __translate_neurological_hist(hist_type: str) -> str:
        hist_neurol = {"Ischemischhemorragisch_CVA_of_TIA": "Cerebro Vascular Accident or Transient Ischemic Attack",
                           "SAB": "Subarachnoid hemorrhage", "Dementie": "Dementia", "Parkinson": "Parkinson's Disease"}
        return hist_neurol[hist_type]

    def __translate_metabolic_hist(hist_type: str) -> str:
        hist_metabol = {"Diabetes_type_I":  "Diabetes Mellitus type I",
                        "Diabetes_type_II":  "Diabetes Mellitus type II",
                        "Hypercholestorolemie": "Hypercholesterolemia", 
                        "Hypothyreoidie": "Hypothyroidism",
                        "Hyperthyreoidie": "Hyperthyroidism"}
        return hist_metabol[hist_type]

    def __translate_renal_hist(hist_type: str) -> str:
        hist_renal = {"Chronische_nierinsufficintie": "Chronic renal insufficiency", 
                      "Niertransplantatie": "Kidney transplantation"}

    def __translate_hist_other(abs_history: str) -> str:
        hist_other = {"hist_cardio_dis": "Other cardiovascular disease", "hist_pulm_dis": "Other pulmonary disease",
                      "hist_gastroint": "Other gastrointestinal disease",
                      "hist_neurol": "Other neurological disease",
                      "hist_renal_dis": "Other urigenital disease"}
        return hist_other[abs_history]


    # def _translate_surg_type(surg_type: str) -> str:
    #     surg_tranlate = {}
    #     if surg_type == "AVR (aortaklepvervanging)":
    #         surg_translate = "Aortic Valve Replacement"
    #     elif surg_type == "AVP (aortaklepplastiek)":
    #         surg_translate = "Aortic Valve Repair"
    #     elif surg_type == "MVR (mitraalklepvervanging)":
    #         surg_translate = "Mitral Valve Replacement"
    #     elif surg_type == "MVP (mitraalklepplastiek)":
    #         surg_translate = "Mitral Valve Repair"
    #     elif surg_type == "TVR (tricuspidaalklepvervanging)":
    #         surg_translate = "Tricuspid Valve Replacement"
    #     elif surg_type == "TVP (mitraalklepplastiek)":
    #         surg_translate = "Tricuspid Valve Repair"
    #     elif surg_type == "Klepbesparende ascendensvervanging":
    #         surg_translate = "Valve-Sparing Root Replacement (VSRR)"
    #     elif surg_type == "Klep-en ascendensvervanging (Bentall procedure)":
    #         surg_translate = "Bentall procedure"
    #     elif surg_type == "Ascendens-en boogvervanging (Elephant trunk)":
    #         surg_translate = "Elephant trunk procedure"
    #     elif surg_type == "PEARS":
    #         surg_translate = "Personalized External Aortic Root Support (PEARS)"
    #     elif surg_type ==  "Mini-MVP":
    #         surg_translate = "Mini mitral valve repair"
    #     elif surg_type == "Myxoomresectie":
    #         surg_translate = "Myxoma Resection"
    #     elif surg_type == "Myextomie septum":
    #         surg_translate = "Septal Myectomy"
    #     elif surg_type == "ASD-sluiting":
    #         surg_translate = "Atrial septal defect closure"
    #     elif surg_type == "VSD-sluiting":
    #         surg_translate = "Ventricular septal defect closure"
    #     else:
    #         surg_translate = surg_type
    #     return surg_translate

    # def __translate_cardiovascular_hist(hist_type: str) -> str:
        # if hist_type == "Hypertensie":
        #     hist_cardio = "Hypertension"
        # elif hist_type == "Coronairlijden":
        #     hist_cardio = "Coronary disease"
        # elif hist_type == "Decompensatio_cordi":
        #     hist_cardio = "Cordial decompensation"
        # elif hist_type == "Atriumfibrilleren":
        #     hist_cardio = "Atrial fibrillation"
        # elif hist_type == "PacemakerICD":
        #     hist_cardio = "Pacemaker or ICD"
        # elif hist_type == "Open_AAA__repair":
        #     hist_cardio = "Abdominal Aortic Aneurysm Repair (AAA)"
        # elif hist_type == "TEVAR":
        #     hist_cardio = "Thoracic Endovascular Aneurysm Repair (TEVAR)"
        # elif hist_type == "CABG":
        #     hist_cardio = "Coronary Artery Bypass Grafting (CABG)"
        # elif hist_type == "klepvervanging":
        #     hist_cardio = "Valve replacement"
        # elif hist_type == "BentallDavid_procedure":
        #     hist_cardio = "Bentall/David procedure"
        # return hist_cardio

    # def __translate_hist_other(abs_history: str) -> str:
    #     if abs_history == "hist_cardio_dis":
    #         other_history = "Other cardiovascular disease"
    #     elif abs_history == "hist_pulm_dis":
    #         other_history = "Other pulmonary disease"
    #     elif abs_history == "hist_gastroint":
    #         other_history = "Other gastrointestinal disease"
    #     elif abs_history == "hist_neurol":
    #         other_history = "Other neurological disease"
    #     elif abs_history == "hist_renal_dis":
    #         other_history = "Other urigenital disease"
    #     return other_history

    # def __translate_gastorintestinal_hist(hist_type: str) -> str:   
        # if hist_type == "Peptisch_ulcus":
        #     hist_GI = "Peptic ulcer"
        # elif hist_type == "GIbloeding":
        #     hist_GI = "Gastrointestinal bleeding"
        # elif hist_type == "IBD_Crohncolitis_ulcerose":
        #     hist_GI = "Inflammatory bowel disease (Crohn/Colitis ulcerosa)"
        # elif hist_type == "Leverziekte_bijv_hepatitis_cirrose_NAFLD":
        #     hist_GI = "Liver disease"

    # def __translate_pulmonary_hist(hist_type: str) -> str:
    #     if hist_type == "Astma":
    #         hist_pulm = "Asthma"
    #     elif hist_type == "COPD":
    #         hist_pulm = "COPD"
    #     elif hist_type == "Longembolie":
    #         hist_pulm = "Pulmonary embolism"
    #     return hist_pulm