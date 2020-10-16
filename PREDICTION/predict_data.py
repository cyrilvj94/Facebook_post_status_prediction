import pickle
import os
import pandas as pd
import shutil
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s :  %(message)s')
file_handler = logging.FileHandler('LOGS/Prediction_logs/prediction_log.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Predict:
    """
    Description: To predict the input file
    :parameter: Preprocessed data
    """
    def __init__(self, X):
        self.X = X
        #with open('tuned_model.pkl', 'rb') as f:  # for using tuned model
        #    self.model = pickle.load(f)
        with open('untuned_model.pkl', 'rb') as f:          #for using untuned model
            self.model = pickle.load(f)
        self.result_path = 'Prediction_Results/prediction.csv'
        logger.info("Instance initiated")
        logger.info("Loaded the existing model.pkl file")

    def predict(self):
        """
        Description:"Predicts the results and save the prediction file to a new directory
        """
        out = self.model.predict(self.X.values)
        logger.info("Prediction obtained")
        preds = pd.DataFrame(out, columns = ['Predictions'])
        #print(preds)
        try:
            if os.path.isdir(self.result_path):# if directory already exists
                shutil.rmtree(self.result_path)
                os.makedirs(self.result_path)
                preds.to_csv(self.result_path, index = False)
                logger.info('Predictions exported to {}'.format(self.result_path))
                preds['Predictions'] = preds.Prediction.map({0:'IA' ,1:'NA',2:'MA',3:'A'})
                return  "Prediction files generated at {}".format(self.result_path), preds.Predictions.to_numpy()

            else:
                preds.to_csv(self.result_path, index=False)
                logger.info('Predictions exported to {}'.format(self.result_path))


                return  "Prediction files generated at {}".format(self.result_path), preds.Predictions.to_numpy()

        except Exception as e:
            logger.info('Error occured while prediction')
            raise e



