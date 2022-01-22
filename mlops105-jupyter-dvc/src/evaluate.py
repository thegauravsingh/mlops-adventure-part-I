import json
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score
import joblib
from sklearn.preprocessing import LabelEncoder

if __name__ == '__main__':
    
    classes = pd.read_csv('data/iris.csv')['species'].unique().tolist()
    test_dataset = pd.read_csv('data/test.csv')
    le = LabelEncoder()
    test_dataset['species'] = le.fit_transform(test_dataset['species'])
    y = test_dataset['species']
    X = test_dataset.drop(columns=['species'])
    
    clf = joblib.load('data/model.joblib')
    
    prediction = clf.predict(X)
    cm = confusion_matrix(prediction, y)
    f1 = f1_score(y_true=y, y_pred=prediction, average='macro')

    json.dump(
        obj={
            'f1_score': f1,
            'confusion_matrix': {
                'classes': classes,
                'matrix': cm.tolist()
            }
        },
        fp=open('data/eval.txt', 'w')
    )