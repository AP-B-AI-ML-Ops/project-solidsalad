import os
from kaggle.api.kaggle_api_extended import KaggleApi
from prefect import task, flow

DATALIMIT = 100


@task
def authenticate_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    print("kaggle api authenticated")
    return api


@task(retries=4, retry_delay_seconds=2)
def download_dataset(api, dataset: str, data_path: str):
    api.dataset_download_files(dataset, path=data_path, unzip=True)
    print("dataset downloaded")


@flow
def collect_flow(data_path: str, update=False):
    os.makedirs(data_path, exist_ok=True)
    api = authenticate_kaggle_api()

    if (not os.path.exists(data_path + "/Mental Health Dataset.csv")) or update:
        download_dataset(api, "bhavikjikadara/mental-health-dataset", data_path)
    else:
        print("dataset already present")
