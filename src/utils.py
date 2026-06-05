import os
import numpy as np
import pandas as pd
import sys
import dill
from src.exception import CustomException
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score


def save_obj(file_path,obj):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)


def evaluate_models(X_train,X_test,y_train,y_test,models):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(X_train, y_train) # Train model

            # Make predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            # Evaluate Train and Test dataset
            model_train_r2 = r2_score(y_train, y_train_pred)

            model_test_r2 = r2_score(y_test, y_test_pred)
            
            report[list(models.keys())[i]] = model_test_r2
            
        return report
        
    except Exception as e:
        raise CustomException(e,sys)
