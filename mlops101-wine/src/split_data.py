#split data
#save data into processed folder


import os
from get_data import read_params, read_file
import argparse
import pandas as pd 
from sklearn.model_selection import train_test_split


def split_data(config_path):
    config = read_params(config_path)
    raw_dataset_csv = config["load_data"]["raw_dataset_csv"]
    test_data_csv = config["split_data"]["test_data_csv"] 
    train_data_csv = config["split_data"]["train_data_csv"] 
    test_size = config["split_data"]["test_size"] 
    random_state = config["base"]["random_state"] 

    df = pd.read_csv(raw_dataset_csv,sep=",",encoding='utf-8')

    train, test = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state
    )

    test.to_csv(test_data_csv, sep=",", index=False, encoding="utf-8")
    train.to_csv(train_data_csv, sep=",", index=False, encoding="utf-8")    

    #print(test.head())
    #print(train.head())

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config_path", default="params.yaml")
    parsed_args = args.parse_args() 
    split_data(config_path=parsed_args.config_path)        