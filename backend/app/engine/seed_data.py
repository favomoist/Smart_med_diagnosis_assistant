"""Clinical knowledge base seed data for symptoms, conditions, mappings, and red flags."""

SYMPTOMS_DATA = [
    {
        "code": "chest_pain",
        "name": "Chest Pain / Pressure",
        "category": "Cardiovascular",
        "is_red_flag": True,
        "guidance": "May indicate acute coronary syndrome, angina, pulmonary embolism, or musculoskeletal strain.",
        "description": "Pain, pressure, tightness, or squeezing sensation across the chest or sternum."
    },
    {
        "code": "shortness_of_breath",
        "name": "Shortness of Breath (Dyspnea)",
        "category": "Respiratory",
        "is_red_flag": True,
        "guidance": "May indicate severe asthma, pneumonia, COPD exacerbation, pulmonary embolism, or heart failure.",
        "description": "Difficulty catching breath, rapid breathing, or feeling suffocated."
    },
    {
        "code": "facial_droop_slurred_speech",
        "name": "Facial Droop / Slurred Speech / Arm Weakness",
        "category": "Neurological",
        "is_red_flag": True,
        "guidance": "FAST protocol emergency marker for acute cerebrovascular accident (stroke).",
        "description": "Sudden asymmetry in the face, difficulty articulating words, or sudden loss of strength in one arm."
    },
    {
        "code": "stiff_neck_fever",
        "name": "High Fever with Stiff Neck & Photophobia",
        "category": "Neurological",
        "is_red_flag": True,
        "guidance": "Hallmark clinical triad for acute bacterial or viral meningitis.",
        "description": "Inability to flex chin to chest combined with elevated temperature and light sensitivity."
    },
    {
        "code": "severe_acute_abdomen",
        "name": "Severe Acute Abdominal Pain",
        "category": "Gastrointestinal",
        "is_red_flag": True,
        "guidance": "Signs of peritonitis, acute appendicitis, or bowel perforation.",
        "description": "Intense, sudden localized or generalized abdominal pain with guarding or rebound tenderness."
    },
    {
        "code": "fever",
        "name": "Fever / Elevated Body Temperature",
        "category": "General",
        "is_red_flag": False,
        "guidance": "Systemic inflammatory or immune response to infection or illness.",
        "description": "Body temperature above 38°C (100.4°F), often accompanied by chills or sweating."
    },
    {
        "code": "cough",
        "name": "Cough",
        "category": "Respiratory",
        "is_red_flag": False,
        "guidance": "Reflex action to clear airways; can be dry, hacking, or productive of phlegm.",
        "description": "Persistent coughing fits, tickle in throat, or chest congestion."
    },
    {
        "code": "sore_throat",
        "name": "Sore Throat (Pharyngitis)",
        "category": "ENT",
        "is_red_flag": False,
        "guidance": "Inflammation of the pharynx or tonsils, commonly viral or bacterial (Strep).",
        "description": "Scratchy, painful sensation in the throat exacerbated by swallowing."
    },
    {
        "code": "headache",
        "name": "Headache",
        "category": "Neurological",
        "is_red_flag": False,
        "guidance": "Can range from tension headaches to migraine or sinus congestion.",
        "description": "Aching or throbbing pain in the forehead, temples, or base of the skull."
    },
    {
        "code": "nasal_congestion",
        "name": "Runny / Stuffy Nose (Rhinorrhea)",
        "category": "ENT",
        "is_red_flag": False,
        "guidance": "Mucosal swelling and discharge due to viral infection or allergies.",
        "description": "Blockage of nasal passages, clear or discolored mucus drainage."
    },
    {
        "code": "fatigue",
        "name": "Fatigue / Lethargy",
        "category": "General",
        "is_red_flag": False,
        "guidance": "Overall lack of energy and persistent feeling of exhaustion.",
        "description": "Generalized physical and mental tiredness not resolved by sleep."
    },
    {
        "code": "nausea_vomiting",
        "name": "Nausea / Vomiting",
        "category": "Gastrointestinal",
        "is_red_flag": False,
        "guidance": "Gastric irritation or systemic malaise leading to emesis.",
        "description": "Queasiness in stomach and involuntary ejection of stomach contents."
    },
    {
        "code": "diarrhea",
        "name": "Diarrhea",
        "category": "Gastrointestinal",
        "is_red_flag": False,
        "guidance": "Frequent loose or watery stools, often due to gastroenteritis or foodborne illness.",
        "description": "Three or more loose/liquid bowel movements per day."
    },
    {
        "code": "muscle_aches",
        "name": "Body Aches (Myalgia)",
        "category": "General",
        "is_red_flag": False,
        "guidance": "Widespread muscular discomfort typical of systemic viral infections like Influenza or COVID-19.",
        "description": "Aching, sore, or tender muscles throughout the body."
    },
    {
        "code": "loss_of_taste_smell",
        "name": "Loss of Smell or Taste (Anosmia / Ageusia)",
        "category": "ENT",
        "is_red_flag": False,
        "guidance": "Frequently associated with respiratory viral pathogens such as SARS-CoV-2.",
        "description": "Sudden partial or complete inability to detect odors or flavors."
    },
    {
        "code": "wheezing",
        "name": "Wheezing",
        "category": "Respiratory",
        "is_red_flag": False,
        "guidance": "Narrowing of the bronchial airways, commonly in asthma, bronchitis, or allergic reaction.",
        "description": "High-pitched musical whistling sound during breathing."
    },
    {
        "code": "joint_pain",
        "name": "Joint Pain (Arthralgia)",
        "category": "Musculoskeletal",
        "is_red_flag": False,
        "guidance": "Aching or stiffness in joints such as knees, wrists, or shoulders.",
        "description": "Pain, stiffness, or slight swelling in joint articulations."
    }
]

CONDITIONS_DATA = [
    {
        "code": "cond_mi",
        "name": "Acute Myocardial Infarction (Heart Attack)",
        "category": "Cardiovascular",
        "typical_urgency": "emergency",
        "description": "Ischemia and necrosis of heart muscle due to blocked coronary arteries.",
        "advice": "CRITICAL EMERGENCY: Call 911 or your local emergency number immediately. Do not attempt to drive yourself to the hospital.",
        "care_recommendations": "Remain seated in a comfortable upright position. Chew 325mg non-enteric aspirin if advised by emergency services and not allergic."
    },
    {
        "code": "cond_stroke",
        "name": "Acute Ischemic Stroke / CVA",
        "category": "Neurological",
        "typical_urgency": "emergency",
        "description": "Disruption of blood supply to the brain causing rapid neurological deficit.",
        "advice": "CRITICAL EMERGENCY: Time-sensitive emergency. Call emergency services immediately. Note exact time symptoms began.",
        "care_recommendations": "Do not give the patient anything to eat or drink. Keep patient lying down with head slightly elevated."
    },
    {
        "code": "cond_meningitis",
        "name": "Acute Bacterial / Viral Meningitis",
        "category": "Neurological",
        "typical_urgency": "emergency",
        "description": "Inflammation of the protective membranes covering the brain and spinal cord.",
        "advice": "EMERGENCY: Immediate emergency hospital admission required for diagnostic workup and intravenous therapy.",
        "care_recommendations": "Proceed directly to the nearest emergency department."
    },
    {
        "code": "cond_covid19",
        "name": "COVID-19 (SARS-CoV-2 Infection)",
        "category": "Infectious Disease",
        "typical_urgency": "urgent_care",
        "description": "Contagious respiratory illness caused by the coronavirus SARS-CoV-2.",
        "advice": "Isolate from others, monitor oxygen levels with a pulse oximeter, and consult a healthcare provider if experiencing difficulty breathing.",
        "care_recommendations": "Rest, maintain vigorous hydration, take over-the-counter antipyretics (acetaminophen/ibuprofen), and perform a rapid antigen test."
    },
    {
        "code": "cond_influenza",
        "name": "Influenza (Seasonal Flu)",
        "category": "Infectious Disease",
        "typical_urgency": "urgent_care",
        "description": "Acute viral infection characterized by sudden onset of high fever, myalgia, and respiratory symptoms.",
        "advice": "Consult a healthcare provider or urgent care within 48 hours if antiviral medications (e.g. oseltamivir) are considered.",
        "care_recommendations": "Strict bed rest, copious fluid intake, fever reducers, warm broths, and humidity."
    },
    {
        "code": "cond_common_cold",
        "name": "Common Cold (Viral Rhinitis)",
        "category": "Infectious Disease",
        "typical_urgency": "self_care",
        "description": "Mild viral upper respiratory tract infection predominantly affecting the nose and throat.",
        "advice": "Self-limiting condition that typically resolves on its own in 7 to 10 days.",
        "care_recommendations": "Saline nasal irrigation, honey for cough relief (in adults/children >1 yr), throat lozenges, and plentiful fluids."
    },
    {
        "code": "cond_strep_throat",
        "name": "Streptococcal Pharyngitis (Strep Throat)",
        "category": "ENT",
        "typical_urgency": "urgent_care",
        "description": "Bacterial infection of the tonsils and throat caused by Group A Streptococcus.",
        "advice": "Schedule an urgent care or clinic appointment for a rapid strep swab to determine if antibiotics are required.",
        "care_recommendations": "Warm salt water gargles, soft foods, throat numbing sprays, and analgesics for pain."
    },
    {
        "code": "cond_migraine",
        "name": "Migraine Headache",
        "category": "Neurological",
        "typical_urgency": "self_care",
        "description": "Recurrent neurological disorder characterized by moderate-to-severe unilateral pulsating headache.",
        "advice": "Manage in a quiet, dark environment. If symptoms are atypical or severe, consult a neurologist or doctor.",
        "care_recommendations": "Apply cool compress to forehead, stay hydrated, take prescribed triptans or OTC NSAIDs at symptom onset."
    },
    {
        "code": "cond_tension_headache",
        "name": "Tension-Type Headache",
        "category": "Neurological",
        "typical_urgency": "self_care",
        "description": "Most common type of headache, presenting as a dull, constant band-like ache around the head.",
        "advice": "Can be managed at home with posture correction, relaxation, and over-the-counter pain relief.",
        "care_recommendations": "Hydration, neck and shoulder stretches, brief nap, stress reduction, and ibuprofen or acetaminophen."
    },
    {
        "code": "cond_gastroenteritis",
        "name": "Acute Viral Gastroenteritis (Stomach Bug)",
        "category": "Gastrointestinal",
        "typical_urgency": "self_care",
        "description": "Inflammation of the stomach and intestines leading to diarrhea, cramping, and vomiting.",
        "advice": "Focus primarily on electrolyte replacement. Seek urgent care if unable to keep liquids down for 24 hours.",
        "care_recommendations": "Sip Oral Rehydration Salts (ORS) or diluted electrolyte drinks slowly. Follow BRAT diet (bananas, rice, applesauce, toast)."
    },
    {
        "code": "cond_allergic_rhinitis",
        "name": "Allergic Rhinitis (Hay Fever)",
        "category": "Immunology",
        "typical_urgency": "self_care",
        "description": "Allergic reaction in the nasal passages caused by airborne allergens like pollen or dust.",
        "advice": "Manage symptoms with over-the-counter allergy medications and environmental allergen control.",
        "care_recommendations": "Second-generation oral antihistamines (cetirizine, fexofenadine), steroid nasal spray, rinse eyes with artificial tears."
    },
    {
        "code": "cond_bronchitis",
        "name": "Acute Bronchitis",
        "category": "Respiratory",
        "typical_urgency": "urgent_care",
        "description": "Inflammation of the bronchial tubes leading to persistent cough and mucus production.",
        "advice": "Consult a healthcare clinician if wheezing occurs or if cough persists longer than 3 weeks.",
        "care_recommendations": "Use a room cool mist humidifier, drink warm herbal teas with honey, and avoid exposure to smoke and air irritants."
    }
]

MAPS_DATA = [
    # Heart Attack
    {"symptom_code": "chest_pain", "condition_code": "cond_mi", "weight": 9.5, "is_hallmark": True},
    {"symptom_code": "shortness_of_breath", "condition_code": "cond_mi", "weight": 8.0, "is_hallmark": False},
    {"symptom_code": "fatigue", "condition_code": "cond_mi", "weight": 5.0, "is_hallmark": False},
    {"symptom_code": "nausea_vomiting", "condition_code": "cond_mi", "weight": 4.5, "is_hallmark": False},

    # Stroke
    {"symptom_code": "facial_droop_slurred_speech", "condition_code": "cond_stroke", "weight": 10.0, "is_hallmark": True},
    {"symptom_code": "headache", "condition_code": "cond_stroke", "weight": 6.0, "is_hallmark": False},

    # Meningitis
    {"symptom_code": "stiff_neck_fever", "condition_code": "cond_meningitis", "weight": 10.0, "is_hallmark": True},
    {"symptom_code": "fever", "condition_code": "cond_meningitis", "weight": 8.5, "is_hallmark": True},
    {"symptom_code": "headache", "condition_code": "cond_meningitis", "weight": 8.0, "is_hallmark": True},
    {"symptom_code": "nausea_vomiting", "condition_code": "cond_meningitis", "weight": 6.0, "is_hallmark": False},

    # COVID-19
    {"symptom_code": "fever", "condition_code": "cond_covid19", "weight": 7.5, "is_hallmark": False},
    {"symptom_code": "cough", "condition_code": "cond_covid19", "weight": 8.0, "is_hallmark": False},
    {"symptom_code": "loss_of_taste_smell", "condition_code": "cond_covid19", "weight": 9.5, "is_hallmark": True},
    {"symptom_code": "fatigue", "condition_code": "cond_covid19", "weight": 7.0, "is_hallmark": False},
    {"symptom_code": "muscle_aches", "condition_code": "cond_covid19", "weight": 7.0, "is_hallmark": False},
    {"symptom_code": "shortness_of_breath", "condition_code": "cond_covid19", "weight": 6.5, "is_hallmark": False},
    {"symptom_code": "sore_throat", "condition_code": "cond_covid19", "weight": 6.0, "is_hallmark": False},

    # Influenza
    {"symptom_code": "fever", "condition_code": "cond_influenza", "weight": 8.5, "is_hallmark": True},
    {"symptom_code": "muscle_aches", "condition_code": "cond_influenza", "weight": 8.5, "is_hallmark": True},
    {"symptom_code": "fatigue", "condition_code": "cond_influenza", "weight": 8.0, "is_hallmark": False},
    {"symptom_code": "cough", "condition_code": "cond_influenza", "weight": 7.0, "is_hallmark": False},
    {"symptom_code": "headache", "condition_code": "cond_influenza", "weight": 6.5, "is_hallmark": False},
    {"symptom_code": "sore_throat", "condition_code": "cond_influenza", "weight": 5.5, "is_hallmark": False},

    # Common Cold
    {"symptom_code": "nasal_congestion", "condition_code": "cond_common_cold", "weight": 9.0, "is_hallmark": True},
    {"symptom_code": "sore_throat", "condition_code": "cond_common_cold", "weight": 7.5, "is_hallmark": False},
    {"symptom_code": "cough", "condition_code": "cond_common_cold", "weight": 6.5, "is_hallmark": False},
    {"symptom_code": "fatigue", "condition_code": "cond_common_cold", "weight": 4.0, "is_hallmark": False},
    {"symptom_code": "headache", "condition_code": "cond_common_cold", "weight": 4.0, "is_hallmark": False},

    # Strep Throat
    {"symptom_code": "sore_throat", "condition_code": "cond_strep_throat", "weight": 9.5, "is_hallmark": True},
    {"symptom_code": "fever", "condition_code": "cond_strep_throat", "weight": 7.5, "is_hallmark": False},
    {"symptom_code": "headache", "condition_code": "cond_strep_throat", "weight": 5.0, "is_hallmark": False},

    # Migraine
    {"symptom_code": "headache", "condition_code": "cond_migraine", "weight": 9.5, "is_hallmark": True},
    {"symptom_code": "nausea_vomiting", "condition_code": "cond_migraine", "weight": 7.5, "is_hallmark": False},
    {"symptom_code": "fatigue", "condition_code": "cond_migraine", "weight": 5.0, "is_hallmark": False},

    # Tension Headache
    {"symptom_code": "headache", "condition_code": "cond_tension_headache", "weight": 9.0, "is_hallmark": True},
    {"symptom_code": "fatigue", "condition_code": "cond_tension_headache", "weight": 4.5, "is_hallmark": False},

    # Gastroenteritis
    {"symptom_code": "diarrhea", "condition_code": "cond_gastroenteritis", "weight": 9.5, "is_hallmark": True},
    {"symptom_code": "nausea_vomiting", "condition_code": "cond_gastroenteritis", "weight": 9.0, "is_hallmark": True},
    {"symptom_code": "fever", "condition_code": "cond_gastroenteritis", "weight": 5.0, "is_hallmark": False},
    {"symptom_code": "fatigue", "condition_code": "cond_gastroenteritis", "weight": 5.0, "is_hallmark": False},

    # Allergic Rhinitis
    {"symptom_code": "nasal_congestion", "condition_code": "cond_allergic_rhinitis", "weight": 9.0, "is_hallmark": True},
    {"symptom_code": "fatigue", "condition_code": "cond_allergic_rhinitis", "weight": 4.0, "is_hallmark": False},

    # Acute Bronchitis
    {"symptom_code": "cough", "condition_code": "cond_bronchitis", "weight": 9.5, "is_hallmark": True},
    {"symptom_code": "wheezing", "condition_code": "cond_bronchitis", "weight": 7.5, "is_hallmark": False},
    {"symptom_code": "fatigue", "condition_code": "cond_bronchitis", "weight": 5.5, "is_hallmark": False},
    {"symptom_code": "chest_pain", "condition_code": "cond_bronchitis", "weight": 4.0, "is_hallmark": False},
]

RED_FLAGS_DATA = [
    {
        "trigger_keyword": "chest pain",
        "warning_message": "Reported chest pain/pressure which may indicate acute coronary syndrome or emergency cardiovascular events.",
        "emergency_instructions": "Call 911 / Emergency Services immediately. Avoid physical exertion."
    },
    {
        "trigger_keyword": "chest pressure",
        "warning_message": "Reported crushing chest pressure. High risk of acute myocardial infarction.",
        "emergency_instructions": "Call 911 / Emergency Services immediately."
    },
    {
        "trigger_keyword": "shortness of breath",
        "warning_message": "Acute shortness of breath or respiratory distress.",
        "emergency_instructions": "Seek urgent emergency medical evaluation immediately."
    },
    {
        "trigger_keyword": "slurred speech",
        "warning_message": "FAST marker: Slurred speech or sudden neurological deficit.",
        "emergency_instructions": "Immediate emergency evaluation for potential stroke (CVA)."
    },
    {
        "trigger_keyword": "facial droop",
        "warning_message": "FAST marker: Sudden facial asymmetry or droop.",
        "emergency_instructions": "Immediate emergency evaluation for potential stroke (CVA)."
    },
    {
        "trigger_keyword": "arm weakness",
        "warning_message": "FAST marker: Sudden unilateral arm weakness or hemiparesis.",
        "emergency_instructions": "Immediate emergency evaluation for potential stroke (CVA)."
    },
    {
        "trigger_keyword": "stiff neck with fever",
        "warning_message": "Classic meningeal irritation sign with elevated temperature.",
        "emergency_instructions": "Proceed immediately to the nearest Emergency Department."
    },
    {
        "trigger_keyword": "severe abdominal pain",
        "warning_message": "Acute severe abdominal pain with potential for peritonitis or appendiceal rupture.",
        "emergency_instructions": "Seek emergency hospital care immediately."
    },
    {
        "trigger_keyword": "coughing blood",
        "warning_message": "Hemoptysis / coughing blood represents a major clinical red flag.",
        "emergency_instructions": "Seek emergency medical assessment immediately."
    }
]
