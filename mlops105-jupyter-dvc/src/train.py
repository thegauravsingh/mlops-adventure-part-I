import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.preprocessing import LabelEncoder


if __name__ == '__main__':

    # Load train set
    train_dataset = pd.read_csv('data/train.csv')
    le = LabelEncoder()
    train_dataset['species'] = le.fit_transform(train_dataset['species'])
    # Get X and Y
    y = train_dataset['species']
    X = train_dataset.drop(columns=['species'])

    # Create an instance of Logistic Regression Classifier and fit the data.
    clf = LogisticRegression(C=0.01, solver='lbfgs', multi_class='multinomial', max_iter=100)
    clf.fit(X, y)

    joblib.dump(clf, 'data/model.joblib')