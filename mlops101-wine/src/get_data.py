#read params
#process
#return df

import os
import yaml
import pandas as pd
import argparse


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def read_file(config_path):
    config = read_params(config_path)
    file_path = config["data_source"]["s3_source"]
    df = pd.read_csv(file_path,sep=",",encoding='utf-8')
    return df

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config_path", default="params.yaml")
    parsed_args = args.parse_args()
    data = read_file(config_path=parsed_args.config_path)
    #print(data)