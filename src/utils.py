import os
import numpy as np
import pandas as pd
import sys
import dill
from src.exception import CustomException
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.model_selection import GridSearchCV

def save_obj(file_path,obj):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)


def evaluate_models(X_train,X_test,y_train,y_test,models,params):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            grid_object = GridSearchCV(model,param,cv=3)
            grid_object.fit(X_train,y_train)

            model.set_params(**grid_object.best_params_)
            model.fit(X_train,y_train)
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
