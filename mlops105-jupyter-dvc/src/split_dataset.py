import argparse
import pandas as pd

from sklearn.model_selection import train_test_split
import yaml

params = yaml.safe_load(open("params.yaml"))["stage_split_dataset"]

if __name__ == '__main__':
    
    test_size = params['test_size']
    dataset = pd.read_csv('data/iris_featurized.csv')
    
    # transform targets (species) to numerics
    # dataset.loc[dataset.species=='setosa', 'species'] = 0
    # dataset.loc[dataset.species=='versicolor', 'species'] = 1
    # dataset.loc[dataset.species=='virginica', 'species'] = 2
    
    # Split in train/test

    df_train, df_test = train_test_split(dataset, test_size=test_size, random_state=42)
    
    df_train.to_csv('data/train.csv', index=False)
    df_test.to_csv('data/test.csv', index=False)
    
