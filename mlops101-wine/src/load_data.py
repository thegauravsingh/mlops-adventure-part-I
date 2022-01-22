# read the data 
# save it in data/raw 


import os
from get_data import read_params, read_file
import argparse

def load_and_save(config_path):
    config = read_params(config_path)
    df = read_file(config_path)
    new_cols = [col.replace(" ","_") for col in df.columns]
    raw_dataset_csv = config["load_data"]["raw_dataset_csv"]
    df.to_csv(raw_dataset_csv, sep=",", index=False, header=new_cols)
    #print(new_cols)
    #print(df.head())
 
if __name__== "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config_path", default="params.yaml")
    parsed_args = args.parse_args() 
    load_and_save(config_path=parsed_args.config_path)