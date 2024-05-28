pip install prefect
pip install kaggle
pip install mlflow
pip install optuna
prefect server start
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
./exercise/run_servers.sh
python exercise/main.py