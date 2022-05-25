from dataclasses import dataclass

@dataclass
class Translate:

    def _translate_surg_type(surg_type: str) -> str:
        if surg_type == "AVR (aortaklepvervanging)":
            surg_translate = "Aortic Valve Replacement"
        elif surg_type == "AVP (aortaklepplastiek)":
            surg_translate = "Aortic Valve Repair"
        elif surg_type == "MVR (mitraalklepvervanging)":
            surg_translate = "Mitral Valve Replacement"
        elif surg_type == "MVP (mitraalklepplastiek)":
            surg_translate = "Mitral Valve Repair"
        elif surg_type == "TVR (tricuspidaalklepvervanging)":
            surg_translate = "Tricuspid Valve Replacement"
        elif surg_type == "TVP (mitraalklepplastiek)":
            surg_translate = "Tricuspid Valve Repair"
        elif surg_type == "Klepbesparende ascendensvervanging":
            surg_translate = "Valve-Sparing Root Replacement (VSRR)"
        elif surg_type == "Klep-en ascendensvervanging (Bentall procedure)":
            surg_translate = "Bentall procedure"
        elif surg_type == "Ascendens-en boogvervanging (Elephant trunk)":
            surg_translate = "Elephant trunk procedure"
        elif surg_type == "PEARS":
            surg_translate = "Personalized External Aortic Root Support (PEARS)"
        elif surg_type ==  "Mini-MVP":
            surg_translate = "Mini mitral valve repair"
        elif surg_type == "Myxoomresectie":
            surg_translate = "Myxoma Resection"
        elif surg_type == "Myextomie septum":
            surg_translate = "Septal Myectomy"
        elif surg_type == "ASD-sluiting":
            surg_translate = "Atrial septal defect closure"
        elif surg_type == "VSD-sluiting":
            surg_translate = "Ventricular septal defect closure"
        else:
            surg_translate = surg_type
        return surg_translate

    def _translate_med_history(hist_type: str) -> str:
        abs_history, spec_history = hist_type.split(sep='#')
        if abs_history == "hist_cardio_dis":
            hist = Translate.__translate_cardiovascular_hist(spec_history)
        # TODO: add all other abs_histories..
       
        
        # In case of overig
        if spec_history.lower() == "overig":
            hist = Translate.__translate_hist_other(abs_history)
    
        return hist
    
    def __translate_cardiovascular_hist(hist_type: str) -> str:
        if hist_type == "Hypertensie":
            hist_cardio = "Hypertension"
        elif hist_type == "Coronairlijden":
            hist_cardio = "Coronary disease"
        elif hist_type == "Decompensatio_cordi":
            hist_cardio = "Cordial decompensation"
        elif hist_type == "Atriumfibrilleren":
            hist_cardio = "Atrial fibrillation"
        elif hist_type == "PacemakerICD":
            hist_cardio = "Pacemaker or ICD"
        elif hist_type == "Open_AAA__repair":
            hist_cardio = "Abdominal Aortic Aneurysm Repair (AAA)"
        elif hist_type == "TEVAR":
            hist_cardio = "Thoracic Endovascular Aneurysm Repair (TEVAR)"
        elif hist_type == "CABG":
            hist_cardio = "Coronary Artery Bypass Grafting (CABG)"
        elif hist_type == "klepvervanging":
            hist_cardio = "Valve replacement"
        elif hist_type == "BentallDavid_procedure":
            hist_cardio = "Bentall/David procedure"
        return hist_cardio

    def __translate_hist_other(abs_history: str) -> str:
        if abs_history == "hist_cardio_dis":
            other_history = "Other cardiovascular disease"
        elif abs_history == "hist_pulm_dis":
            other_history = "Other pulmonary disease"
        elif abs_history == "hist_gastroint":
            other_history = "Other gastrointestinal disease"
        elif abs_history == "hist_neurol":
            other_history = "Other neurological disease"
        elif abs_history == "hist_renal_dis":
            other_history = "Other urigenital disease"
        return other_history