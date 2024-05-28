pip install prefect
pip install kaggle
pip install mlflow
pip install optuna
prefect server start
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
python exercise/main.py