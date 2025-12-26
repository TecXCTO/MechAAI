'''

# First run these following cmd:-

# dvc init
# dvc add data/raw/wool_samples

'''
import mlflow
with mlflow.start_run():
    mlflow.log_param("generation", 5)
    mlflow.log_metric("tensile_strength_accuracy", 0.94)
    mlflow.log_artifact("src/core/models/evolved_models/gen_5_model.py")
