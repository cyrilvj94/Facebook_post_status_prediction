import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score
import xgboost
from sklearn.model_selection import train_test_split
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s :  %(message)s')
file_handler = logging.FileHandler('LOGS/Modelling_logs/modelling_logs.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Modelling:

    """
    Description: This class contains all the methods for modelling , hyper parameter tuning and finally
           export a pickle file
   :parameter: X,features & y,labels
    """
    def __init__(self, features, labels):
        """
        Pycaret requires features and labels in a single dataframe object
        :param features:
        :param labels:
        """
        try:
            self.features = features
            self.labels = labels
            logger.info("Data obtained for training, shaped {} , {}".format(self.features.shape, self.labels.shape))
        except Exception as e:
            logger.error("Error while creting instance : {}".format(e))
            raise e

    def select_best_model(self):
        """
        Description: This function selects the best model from available list and also tunes the model
            and makes a pickle object

        """
        try:
            logger.info("start of modelling")
            x_train, x_test, y_train, y_test = train_test_split(self.features, self.labels)
            rf = RandomForestClassifier(verbose=False)
            xg = xgboost.XGBClassifier(verbose=False)
            models_used = {0: rf, 1: xg}
            rf.fit(x_train, y_train.post_status.values)
            xg.fit(x_train, y_train.post_status.values)
            print(y_train, type(y_train))
            scores = [accuracy_score(y_test, rf.predict(x_test)), accuracy_score(y_test, xg.predict(x_test))]
            scores = np.array(scores)
            logger.info("Accuracy scores for data rf and xgboost {}".format(scores))
            if scores.argmax() == 0:  # rf selected
                model = models_used[scores.argmax()]
                params = {'n_estimators': range(10, 150, 10),
                          'criterion': ['gini', 'entropy'],
                          'max_depth': range(10, 31, 2),
                          'min_samples_split': range(10, 31, 2)
                          }
                tuned_model = RandomizedSearchCV(model, param_distributions=params, cv=10)
                logger.info("Random Forest selected params: {}".format(tuned_model))
            else:
                model = models_used[scores.argmax()]
                params = {'min_child_weight': range(1, 10),
                          'gamma': [0.5, 1, 1.5, 2, 5],
                          'subsample': [0.6, 0.8, 1.0],
                          'colsample_bytree': [0.6, 0.8, 1.0],
                          'max_depth': [3, 4, 5],
                          'learning_rate ': [0.0001, 0.001, 0.01, 0.05]

                          }
                tuned_model = RandomizedSearchCV(model, param_distributions=params, cv=10)
                logger.info("xgboost selected params: {}".format(tuned_model))

            logger.info("END OF MODELLING")
            return tuned_model

        except Exception as e: # fit and tune random forest classifier if pycaret fails
            logger.info("Error in Training model {}".format(e))
            raise e










