import datetime
import time
from dotenv import load_dotenv
import os
import pickle
import pandas as pd
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric
from evidently.metrics import DatasetMissingValuesMetric
from evidently import ColumnMapping
from sklearn.preprocessing import LabelEncoder
import psycopg

load_dotenv()

# Define categorical mappings
BINARY_CATEGORICAL_COLS = ['Gender', 'family_history', 'treatment', 'Coping_Struggles']
THREE_OPTION_CATEGORICAL_COLS = ['self_employed', 'Growing_Stress', 'Changes_Habits', 'Mental_Health_History', 
                                  'Work_Interest', 'Social_Weakness', 'mental_health_interview', 'care_options']
DAYS_MAPPING = {'Go out Every day': 0, '1-14 days': 1, '15-30 days': 2, '31-60 days': 3, 'More than 2 months': 4}

COL_MAPPING = ColumnMapping(
    prediction='Mood_Swings',
    numerical_features=[],
    categorical_features=BINARY_CATEGORICAL_COLS + THREE_OPTION_CATEGORICAL_COLS,
    target='Mood_Swings'
)

# host, port, user, password
CONNECT_STRING = f'host={os.getenv("POSTGRES_HOST")} port={os.getenv("POSTGRES_PORT")} user={os.getenv("POSTGRES_USER")} password={os.getenv("POSTGRES_PASSWORD")}'

def prep_db():
    create_table_query = """
    DROP TABLE IF EXISTS metrics;
    CREATE TABLE metrics(
        timestamp timestamp,
        num_drifted_columns integer,
        share_missing_values float
    );
    """

    with psycopg.connect(CONNECT_STRING, autocommit=True) as conn:
        # zoek naar database genaamd 'test' in de metadata van postgres
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("CREATE DATABASE test;")
        with psycopg.connect(f'{CONNECT_STRING} dbname=test') as conn:
            conn.execute(create_table_query)

def preprocess_data(df):
    df.dropna(inplace=True)
    df.drop(columns=["Timestamp"], inplace=True)
    
    for col in BINARY_CATEGORICAL_COLS:
        df[col] = df[col].map({'Female': 0, 'Male': 1, 'No': 0, 'Yes': 1})
        
    for col in THREE_OPTION_CATEGORICAL_COLS:
        df[col] = df[col].map({'No': 0, 'Maybe': 1, 'Yes': 2, 'nan': -1, 'Not sure': 1})
    
    df['Days_Indoors'] = df['Days_Indoors'].map(DAYS_MAPPING)
    
    label_encoder = LabelEncoder()
    df = df.apply(label_encoder.fit_transform)
    
    return df

def prep_data():
    ref_data = pd.read_csv('data/Mental Health Dataset.csv')
    ref_data = preprocess_data(ref_data)
    with open('models/dv.pkl', 'rb') as f_in:
        dv = pickle.load(f_in)
    
    raw_data = pd.read_csv('data/Mental Health Dataset.csv')
    raw_data = preprocess_data(raw_data)

    return ref_data, dv, raw_data

def calculate_metrics(current_data, dv, ref_data):
    current_data_dict = current_data.to_dict(orient='records')
    current_data_transformed = dv.transform(current_data_dict)
    ref_data_dict = ref_data.to_dict(orient='records')
    ref_data_transformed = dv.transform(ref_data_dict)

    # Ensure columns are aligned
    current_df = pd.DataFrame(current_data_transformed.toarray(), columns=dv.feature_names_)
    ref_df = pd.DataFrame(ref_data_transformed.toarray(), columns=dv.feature_names_)

    report = Report(metrics=[
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
    ])

    report.run(
        reference_data=ref_df,
        current_data=current_df,
        column_mapping=COL_MAPPING
    )

    result = report.as_dict()

    num_drifted_cols = result['metrics'][0]['result']['number_of_drifted_columns']
    share_missing_vals = result['metrics'][1]['result']['current']['share_of_missing_values']

    return num_drifted_cols, share_missing_vals
    
def save_metrics_to_db(cursor, date, num_drifted_cols, share_missing_vals):
    cursor.execute("""
    INSERT INTO metrics(
        timestamp,
        num_drifted_columns,
        share_missing_values
    )
    VALUES (%s, %s, %s);
    """, (date, num_drifted_cols, share_missing_vals))

def monitor():
    startDate = datetime.datetime(2022, 2, 1, 0, 0)
    endDate = datetime.datetime(2022, 2, 2, 0, 0)

    prep_db()

    ref_data, dv, raw_data = prep_data()

    with psycopg.connect(f'{CONNECT_STRING} dbname=test') as conn:
        with conn.cursor() as cursor:
            # Simulate daily data by iterating through rows in chunks
            for i in range(0, 2700, 100):  # Assuming chunk size of 100 for simulation
                current_data = raw_data.iloc[i:i+100]
                
                num_drifted_cols, share_missing_vals = calculate_metrics(current_data, dv, ref_data)
                save_metrics_to_db(cursor, startDate, num_drifted_cols, share_missing_vals)

                startDate += datetime.timedelta(1)
                endDate += datetime.timedelta(1)

                time.sleep(1)
                print("data added")

if __name__ == '__main__':
    monitor()
