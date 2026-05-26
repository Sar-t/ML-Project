import sys
from dataclasses import dataclass #used to declare class variables
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer #missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_obj

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_tranformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            cat_features = [
                'gender', 
                'race_ethnicity', 
                'parental_level_of_education', 
                'lunch', 
                'test_preparation_course'
            ]
            num_features = [
                # math_score is target feature
                'reading_score', 
                'writing_score'
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='median')),
                    ("scaler",StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ("inputer",SimpleImputer(strategy='most_frequent')),
                    ("one_hot_encoder",OneHotEncoder()),
                ]
            )

            logging.info('Categorical Columns encoding completed!')
            logging.info('Numerical Columns scaling completed')

            preprocessor = ColumnTransformer(
                transformers=[
                    ("Numerical Preprocessor",num_pipeline,num_features),
                    ("Categorical Features",cat_pipeline,cat_features)
                ]
            )
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('train and test data read successfully !')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = ['math_score']
            numerical_columns = ['writing_score','reading_score']

            target_feature_train_df = train_df[target_column_name] #y_train
            input_feature_train_df = train_df.drop(columns=target_column_name) #X_train
            

            target_feature_test_df = test_df[target_column_name] #y_test
            input_feature_test_df = test_df.drop(columns=target_column_name) #X_test
            

            logging.info('Applying preprocessing object on train and test dataframe')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df) #on training data the transformers are trained or fit and the train_data is then transform
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df) #the transformers trained on training data are use to transform test data
            #preprocessor returns an array

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]

            logging.info('Saved preprocessing object')

            save_obj(self.data_tranformation_config.preprocessor_obj_file_path,preprocessing_obj)

            return [
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path
            ]

        except Exception as e:
            raise CustomException(e,sys)


