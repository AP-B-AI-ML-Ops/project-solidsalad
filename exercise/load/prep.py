import os
import pickle
import pandas as pd

from prefect import flow, task

from sklearn.calibration import LabelEncoder
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split

@task
def dump_pickle(obj, filename: str):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)

@task
def read_dataframe(filename: str):
    df = pd.read_csv(filename)
    return df

@task
def drop_na(df):
    df.dropna(inplace = True)
    return df

@task
def preprocess(df: pd.DataFrame, dv: DictVectorizer, fit_dv: bool = False):
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
    
    # Combine categorical and numerical columns into dictionaries
    dicts = encoded_df.to_dict(orient='records')
    
    if fit_dv:
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)
    return X, dv


@flow
def prep_flow(data_path: str, dest_path: str):
    df = read_dataframe(
        os.path.join(data_path, "Mental Health Dataset.csv")
    )

    # Extract the target
    target = 'Mood_Swings'
    y = df[target].values

    # Fit the DictVectorizer and preprocess data
    dv = DictVectorizer()
    X, dv = preprocess(df, dv, fit_dv=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

    # Create dest_path folder unless it already exists
    os.makedirs(dest_path, exist_ok=True)

    # Save DictVectorizer and datasets
    dump_pickle(dv, os.path.join(dest_path, "dv.pkl"))
    dump_pickle((X_train, y_train), os.path.join(dest_path, "train.pkl"))
    dump_pickle((X_test, y_test), os.path.join(dest_path, "test.pkl"))