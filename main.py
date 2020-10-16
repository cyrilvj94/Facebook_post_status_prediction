from DATA_VALIDATION.Validation import Train_validation
from DB_OPERATIONS.Database_operations import DB_operation
from flask import Flask,render_template,request,redirect,url_for
from DATA_VALIDATION.Predictoin_file_validation import Prediction_validation
from DATA_PREPROCESSING.Train_preprocessing import  Preprocessing
from PREDICTION.predict_data import Predict
from MODELLING.Model_Creation import Modelling
import pandas as pd
import os
import pickle
import shutil
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s :  %(message)s')
file_handler = logging.FileHandler('LOGS/General_logs.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/train', methods=['POST'])
def train():

    f = request.files.getlist('files')
    for file in f:
        file.save(os.path.join("Raw_Data_Training", file.filename))

    train_file_path = 'Raw_Data_Training'
    d = Train_validation(train_file_path)
    #START OF DATA_VALIDATION
    logger.info("**********************START OF DATA VALIDATION-Training Data****************************")
    col_no, col_names, col_info = d.getvaluesfromjson()
    logger.info("Obtained values from .json file")
    d.create_training_directory()
    logger.info("Training directory Created ")
    d.col_length_validation(col_no)
    logger.info("Columns length Validation of Training batches Completed ")
    d.missing_value_validation()
    logger.info("Missing Value validation of Training batches Completed ")
    logger.info("***************DATA VALIDATIONS COMPLETED SUCCESSFULLY*************************")



    #print(col_no, col_names, col_info)
    ##START OF DB OPERATION
    logger.info("****************START OF DB OPERATIONS********************")
    filepath = 'Training_batches/Good_data' # Directory containing all training batches
    table_name = 'Train'
    output_path = 'Combined_training_data/Input_file.csv'
    db = DB_operation(filepath, table_name, output_path)
    logger.info("Instace Created")
    conn = db.db_conn('FB_post_status')
    logger.info("Connection to DB establised")
    db.create_table(conn, col_info)
    logger.info("Table Created")
    db.insert_values_to_table(conn)
    logger.info("Data inserted to DB")
    db.export_csv(conn)
    logger.info(".csv file exported to {}".format(output_path))
    db.close_connection(conn)
    logger.info("Connection Closed")
    logger.info("************DB OPERATIONS COMPLETED SUCCESSFULLY*********************")

    ##START OF DATA PREPROCESSING


    from DATA_PREPROCESSING.Train_preprocessing import  Preprocessing
    logger.info("********************************START OF DATA PREPROCESSING - TRAIN DATA********************")
    p = Preprocessing(db.output_path, 0)# 0 to denote training since same class is used for prediction
    logger.info('Instance Created')
    p.remove_unwanted_columns()
    logger.info("Unwanted columns removed")
    p.combine_comments()
    logger.info("Derived feature obtained by combining comments")
    p.label_comments_recieved()
    logger.info("Labelled comments_received feature")
    p.seperate_features_labels()
    logger.info("Labels and features seperated")
    p.random_undersampling()
    logger.info("Random Under sampling performed")
    p.encoding_pg_category()
    logger.info("Encoded pg_category column")
    X, y = p.X, p.y
    logger.info("Data preprocessing of train data completed shapes {} {}".format(X.shape, y.shape))
    logger.info("********************************END OF DATA PREPROCESSING - TRAIN DATA********************")

##MODELLING

    logger.info("***********START OF MODELLING******************")
    model = Modelling(X,y)
    m = model.select_best_model()
    logger.info("Model made successfully MODEL {}".format(m))
    with open('model_retrain.pkl', 'wb') as f:
        pickle.dump(m, f)
    logger.info("pickle file 'model.pkl' generated at current working directory")
    logger.info("***********END OF MODELLING******************")
    return render_template('retrain.html')


@app.route('/predict',methods=['POST'])
def upload_file():
    test_file = request.files['filename']
    if os.path.isdir(os.path.join('.', 'Raw_Data_Prediction')): # Remove already existing directories
        shutil.rmtree(os.path.join('.', 'Raw_Data_Prediction'))
        os.makedirs(os.path.join('.', 'Raw_Data_Prediction'))
    if test_file.filename != '':
        test_file.save(os.path.join('.', 'Raw_Data_Prediction', test_file.filename))

    logger.info("**********START OF PREDICTION*************")
    pred_file_path = 'Raw_Data_Prediction'
    pred_val = Prediction_validation(pred_file_path)
    #Start of Data Validation
    logger.info("Start of data vaidation- prediction")
    col_no, col_names, col_info = pred_val.getvaluesfromjson()
    logger.info('Obtained data from .json file')
    pred_val.create_prediction_directory()
    logger.info('Temporary Directory Created')
    pred_val.col_length_validation(col_no)
    logger.info('col. length validated')
    pred_val.missing_value_validation()
    logger.info('Missing value Validated')
    #Database Operations
    path = 'Combined_prediction_data/Input_file.csv'
    pred_filepath = 'Prediction_batches/Good_data'
    for file in os.listdir(pred_filepath):
        data = pd.read_csv(os.path.join(pred_file_path, file))
        data.rename(columns = dict(zip(data.columns, col_names)), inplace = True)
        data.to_csv(path, index  = None)
        print(data)
    logger.info('*************START OF DB OPERATIONS*************')
    """
    pred_filepath = 'Prediction_batches/Good_data' # Directory containing all prediction batches
    pred_table_name = 'Prediction_1'
    pred_output_path = 'Combined_prediction_data/Input_file.csv'
    db_pred = DB_operation(pred_filepath, pred_table_name, pred_output_path)
    conn = db_pred.db_conn('FB_train')
    logger.info('Created connection object')
    db_pred.create_table(conn, col_info)
    logger.info('Table Created')
    db_pred.insert_values_to_table(conn)
    logger.info('Values inserted to table')
    db_pred.export_csv(conn)
    logger.info('Exported the csv file')
    db_pred.close_connection(conn)
    logger.info('Closed the connection')
    """
    shutil.rmtree('Prediction_batches')  ##remove prediction_batches
    #Data preprocessing
    path = 'Combined_prediction_data/Input_file.csv'
    logger.info('**********START OF DATA PREPROCESSING-PREDICTION************')
    prediction_pre = Preprocessing(path, 1) # 1 denotes prediction pipeline
    prediction_pre.remove_unwanted_columns()
    logger.info('Unwanted columns removed')
    prediction_pre.combine_comments()
    logger.info('Obtained Derived features')
    prediction_pre.label_comments_recieved()
    logger.info('labelled_comments_received')
    prediction_pre.seperate_features_labels()
    logger.info('Seperated features and labels')
    #prediction_pre.random_undersampling() # no need for random sampling for prediction files
    prediction_pre.encoding_pg_category()
    logger.info('Encoded pg_category')
    X, y = prediction_pre.X, prediction_pre.y
    pr = Predict(X)
    res,out = pr.predict()
    logger.info('Result obtained in predict.html')
    return render_template('predict.html', prediction= out)

    #Print res in UIreturn render_template('predict.html', prediction = test_file.filename )

if __name__=='__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)


