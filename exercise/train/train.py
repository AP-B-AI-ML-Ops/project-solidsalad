import os
import pickle
import mlflow
from prefect import task, flow

from sklearn.ensemble import RandomForestClassifier


@task
def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@task
def start_ml_experiment(X_train, y_train):
    with mlflow.start_run():
        rf = RandomForestClassifier(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)


@flow
def train_flow(model_path: str, experiment_name: str):
    mlflow.set_experiment(experiment_name)
    mlflow.sklearn.autolog()

    X_train, y_train = load_pickle(os.path.join(model_path, "train.pkl"))

    start_ml_experiment(X_train, y_train)
