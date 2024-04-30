import pandas as pd
import numpy as np


corrected_model_columns = ['Patients number per hour', 'Saturation', 'Length of stay_min',
       'Group_Regional ED (4th Degree)', 'Sex_Male',
       'Arrival mode_Private Ambulance', 'Arrival mode_Private Vehicle',
       'Arrival mode_Public Ambulance', 'Arrival mode_Walking', 'Injury_Yes',
       'Mental_Pain Response', 'Mental_Unresponsive',
       'Mental_Verbose Response', 'Pain_Yes', 'KTAS_RN_Non-Emergency',
       'Disposition_Admission to Ward', 'Disposition_Death',
       'Disposition_Discharge', 'Disposition_Surgery', 'Disposition_Transfer',
       'KTAS_expert_Non-Emergency', 'New_Age_Mid_Age', 'New_Age_Old',
       'New_Age_Young', 'New_SBP_Low', 'New_SBP_Normal', 'New_DBP_Low',
       'New_DBP_Normal', 'New_HR_Low', 'New_HR_Normal', 'New_RR_Low',
       'New_RR_Normal', 'New_BT_Low', 'New_BT_Normal', 'New_NRS_pain_Low Pain',
       'New_NRS_pain_Pain', 'New_KTAS_duration_min_Very Urgent',
       'New_Length_of_stay_min_Non-Urgent', 'New_Length_of_stay_min_Standart',
       'New_Length_of_stay_min_Urgent', 'New_Length_of_stay_min_Very Urgent']

def preprocess_input(raw_input):
    # Mapping the input to DataFrame format similar to the training data
    data = {
        'Sex': [1 if raw_input['sex'].lower() == 'male' else 2],
        'Age': [int(raw_input['age'])],
        'Arrival mode': [int(raw_input['arrival_mode'])],  # assuming numeric mapping available
        'Injury': [1 if 'injury' in raw_input['injury'].lower() else 2],
        'Chief_complain': [raw_input['chief_complaint'].lower()],
        'Mental': [1 if raw_input['mental_state'].lower() == 'normal' else 2],  # simplify for example
        'Pain': [1],
        'NRS_pain': [int(raw_input['pain_intensity'])],
        'SBP': [raw_input['blood_pressure'].split('/')[0]],
        'DBP': [raw_input['blood_pressure'].split('/')[1]],
        'HR': [raw_input['heart_rate']],
        'RR': [15 if raw_input['respiratory_rate'].lower() == 'normal' else 25],  # example mapping
        'BT': [raw_input['body_temperature']]
    }
    
    df = pd.DataFrame(data)
    processed_df = apply_feature_engineering(df)  # Apply the same feature engineering as for training data

    # Add extra processing if required for consistency with model training
    processed_df['Sex_Male'] = (processed_df['Sex'] == 'Male').astype(int)
    processed_df['Injury_Yes'] = (processed_df['Injury'] == 'Yes').astype(int)
    processed_df['Pain_Yes'] = (processed_df['Pain'] == 'Yes').astype(int)
    processed_df['Mental_Pain Response'] = (processed_df['Mental'] == 'Pain Response').astype(int)
    processed_df['Mental_Unresponsive'] = (processed_df['Mental'] == 'Unresponsive').astype(int)
    processed_df['Mental_Verbose Response'] = (processed_df['Mental'] == 'Verbose Response').astype(int)

    # Ensuring only model columns are used
    for col in corrected_model_columns:
        if col not in processed_df.columns:
            processed_df[col] = 0

    return processed_df[corrected_model_columns]


def apply_feature_engineering(df):
    # Categorizing categorical data
    sex_cat = ['Female', 'Male']
    injury_cat = ['No', 'Yes']
    pain_cat = ['No', 'Yes']
    mental_cat = ['Alert', 'Verbose Response', 'Pain Response', 'Unresponsive']

    df['Sex'] = df['Sex'].map({1: sex_cat[0], 2: sex_cat[1]})
    df['Injury'] = df['Injury'].map({1: injury_cat[0], 2: injury_cat[1]})
    df['Pain'] = df['Pain'].map({0: pain_cat[0], 1: pain_cat[1]})
    df['Mental'] = df['Mental'].map({1: mental_cat[0], 2: mental_cat[1], 3: mental_cat[2], 4: mental_cat[3]})

    # Assuming the input for BP, HR, RR, and BT are already string formatted and may contain '??'
    # Replacing '??' with NaN and converting to float
    df[['SBP', 'DBP', 'HR', 'RR', 'BT']] = df[['SBP', 'DBP', 'HR', 'RR', 'BT']].replace('??', np.nan).astype(float)

    # Replacing NaN with median values for continuous variables
    for col in ['SBP', 'DBP', 'HR', 'RR', 'BT']:
        if df[col].isna().any():
            df[col].fillna(df[col].median(), inplace=True)

    return df

raw_input = {
    "sex": "male",
    "arrival_mode": "5", 
    "age": "40",
    "blood_pressure": "80/120",
    "oxygen_saturation": "99%",
    "chief_complaint": "chest pain since morning with itching in my body.",
    "user_id": "test",
    "mental_state": "normal",
    "pain_intensity": "7",
    "heart_rate": "115",
    "respiratory_rate": "normal",
    "injury": "I have minor injury in my neck",
    "body_temperature": "38"
}

# Preprocessing the input
processed_input = preprocess_input(raw_input)
print(processed_input)
