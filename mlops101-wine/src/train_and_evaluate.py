# load train and test dataset
# train algo
# save the metrics , params

from logging.config import fileConfig
import warnings
import sys
import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
from get_data import read_params
import argparse
import joblib
import json
import mlflow
import mlflow.sklearn

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_csv = config["split_data"]["test_data_csv"] 
    train_data_csv = config["split_data"]["train_data_csv"] 
    random_state = config["base"]["random_state"] 
    model_dir = config["model_dir"]

    alpha =  config["estimators"]["ElasticNet"]["params"]["alpha"] 
    l1_ratio =  config["estimators"]["ElasticNet"]["params"]["l1_ratio"] 
    target =  config["base"]["target_col"] 

    train = pd.read_csv(train_data_csv, sep =",")
    test = pd.read_csv(test_data_csv, sep =",")
    
    train_y = train[target]
    test_y =  test[target]

    train_x = train.drop(target, axis=1)
    test_x =  test.drop(target, axis=1)

    remote_server_uri = config["mlflow_config"]["remote_server_uri"]
    experiment_name = config["mlflow_config"]["experiment_name"]
    
    #mlflow.set_registry_uri(remote_server_uri)
    mlflow.set_tracking_uri("http://127.0.0.1:1234")
    #mlflow.set_experiment(experiment_name)
    mlflow.set_experiment("mlflow_demo")
    
    run_name = config["mlflow_config"]["run_nane"]    
    
    #with mlflow.start_run(run_name=run_name) as mlops_run:
    with mlflow.start_run(run_name="LRmodel") as mlops_run:

        lr = ElasticNet(alpha=alpha,l1_ratio=l1_ratio, random_state=random_state)

        lr.fit(train_x,train_y)

        predicted_qualities = lr.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        mlflow.log_param ("alpha", alpha)
        mlflow.log_param ("l1_ratio",l1_ratio)

        mlflow.log_metric("rmse",rmse)
        mlflow.log_metric("mae",mae)
        mlflow.log_metric("r2",r2)        

        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme
        print("tracking_url_type_store ", tracking_url_type_store)
        if tracking_url_type_store != "file":
            #mlflow.sklearn.log_model(
            #    lr,
            #    "model",
            #    registered_model=config["mlflow_config"]["registered_model"], 
            #)
            mlflow.sklearn.log_model(lr, "model", registered_model_name="ElasticnetWineModel")
        else:
            mlflow.sklearn.log_model(lr,"model")



        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)
        scores_file = config["reports"]["scores"]
        params_file = config["reports"]["params"]
        
        with open(scores_file, "w") as f:
            scores = {
                "rmse": rmse,
                "mae": mae,
                "r2": r2
            }
            json.dump(scores, f, indent=4)
        #####################################################
        #with open(params_file, "w") as f:
        #    params = {
        #        "alpha": alpha,
        #        "l1_ratio": l1_ratio,
        #    }
        #    json.dump(params, f, indent=4)
        #####################################################


        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "model.joblib")

        joblib.dump(lr, model_path)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config_path", default="params.yaml")
    parsed_args = args.parse_args() 
    train_and_evaluate(config_path=parsed_args.config_path)        