#i have these columns in a dataset:


#Timestamp
#Gender
#Country
#Occupation
#self_employed
#family_history
#treatment
#Days_Indoors
#Growing_Stress
#Changes_Habits
#Mental_Health_History
#Mood_Swings
#Coping_Struggles
#Work_Interest
#Social_Weakness
#mental_health_interview
#care_options
#
#of w

import pandas as pd
from sklearn.calibration import LabelEncoder

# Load the dataset
file_path = "data/Mental Health Dataset.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print("File not found. Please make sure the file path is correct.")
    exit()

# Display unique values in each column
print("Unique values in each column:")
for column in df.columns:
    unique_values = df[column].unique()
    print("\nColumn:", column)
    for value in unique_values:
        print("-", value)

#dropping timestamp column
df.drop(columns = "Timestamp", inplace = True)

binary_categorical_cols = ['Gender', 'family_history', 'treatment', 'Coping_Struggles']
three_option_categorical_cols = ['self_employed', 'Growing_Stress', 'Changes_Habits', 'Mental_Health_History', 
                                  'Work_Interest', 'Social_Weakness', 'mental_health_interview', 'care_options']

days_mapping = {'Go out Every day': 0, '1-14 days': 1, '15-30 days': 2, '31-60 days': 3, 'More than 2 months': 4}
mood_mapping = {'Low': 0, 'Medium': 1, 'High': 2}

#categorical mapping
for col in binary_categorical_cols:
    df[col] = df[col].map({'Female': 0, 'Male': 1, 'No': 0, 'Yes': 1})
    
for col in three_option_categorical_cols:
    df[col] = df[col].map({'No': 0, 'Maybe': 1, 'Yes': 2, 'nan': -1, 'Not sure': 1})

df['Days_Indoors'] = df['Days_Indoors'].map(days_mapping)
df['Mood_Swings'] = df['Mood_Swings'].map(mood_mapping)

#encoding remaining labels
label_encoder = LabelEncoder()
encoded_df = df.apply(label_encoder.fit_transform)

print(encoded_df.head())