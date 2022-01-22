from sys import _current_frames
import mlflow
from mlflow.tracking import MlflowClient, client
import argparse
import joblib
import os
from pprint import pprint

from mlflow.utils.logging_utils import MLFLOW_LOGGING_STREAM
from get_data import read_params

def tag_models(config_path):
    config = read_params(config_path)
    remote_server_uri = config["mlflow_config"]["remote_server_uri"]
    experiment_name = config["mlflow_config"]["experiment_name"]
    
    #mlflow.set_registry_uri(remote_server_uri)
    mlflow.set_registry_uri("http://127.0.0.1:1234")
    registered_model_name="ElasticnetWineModel"
    experimentName="mlflow_demo"
    experiment = mlflow.get_experiment_by_name("mlflow_demo")
    print(experiment)

    experiment = mlflow.get_experiment(experiment_id=experiment.experiment_id)
    print("Name: {}".format(experiment.name))
    print("Experiment_id: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

    runs = mlflow.search_runs(experiment_ids=experiment.experiment_id)
    print(runs[['run_id','metrics.mae']])
    print(runs.columns)
    lowest = runs["metrics.mae"].sort_values(ascending=True)[0]
    print("lowest ", lowest)
    lowest_run_id = runs[runs["metrics.mae"]==lowest]["run_id"][0]
    print("lowest_run_id ", lowest_run_id)
    client = MlflowClient()
    for mv in client.search_model_versions("name='ElasticnetWineModel'"):
        mv = dict(mv)
        current_version = mv["version"] 
        logged_model = mv["source"]

        print("current_version", current_version)
        print("run_id ", mv["run_id"])
        print("lowest_run_id ", lowest_run_id)
        pprint(mv, indent=4)
        if mv["run_id"] == lowest_run_id:
            client.transition_model_version_stage(
                name=registered_model_name,
                version=current_version,
                stage="Production"
            )
        else:
            client.transition_model_version_stage(
                name=registered_model_name,
                version=current_version,
                stage="staging"
            )


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config_path", default="params.yaml")
    parsed_args = args.parse_args() 
    tag_models(config_path=parsed_args.config_path)        