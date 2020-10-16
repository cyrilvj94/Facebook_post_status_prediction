### 1 . INTRODUCTION AND PROBLEM STATEMENT

The problem statement is to build a Machine Learning
 Classification Model which will predict the status of the
  post being inactive to active in a scale of 0 to 4, 
  0 being inactive and 3 being the most active. 
  The original problem statement was a classification 
  statement to predict the volume of comments a post is 
  expected to receive in the next  ‘h’ hours. 
  Due to insufficiency in dataset to validate
   a regression problem task , as found during E.D.A ,
    the data would be used for a classification problem.
    
### 2 . DATA DESCRIPTION

The Training data comes in the form of batch files.
 There are five training batches .
  Each batch has 53 features and one label. 
  Number of comments received is the labels. 
  The other features are:-
-  Page Features: We identified 4 features of this category that includes features that define the popularity/Likes, category, checkin's and talking about source of document. 
Page likes: It is a feature that defines users support for specific comments, pictures, wall posts,   statuses, or pages. 
Page Category: This defined the category of source of document eg: Local business or place, brand or product, company or institution, artist, band, entertainment,community etc.
 Page Checkin's: It is an act of showing presence at a particular place and under the category of place,institution pages only.
 Page Talking About: This is the actual count of users
  that were ‘ engaged’ and interacting with that
   Facebook Page. The users who actually come back to 
   the page, after liking the page. This includes activities such as comments, likes to a post, shares by visitors to the page.
- Essential Features: This includes the pattern of 
comment on the post in various time intervals w.r.t to the randomly selected base date/time named as C1 to C5. Thee are cumulative comments obtained at different points of time
- Weekday Features: Binary indicators (0,1) are use to represent the day on which the post was published and the day on selected base date/time. 14 features of this type are identified.
- Other Basic Features: This include some documents related features like length of document, time gap between selected base date/time and document published date/time ranges from (0,71), document promotion status values (0,1)and post share count. 5 features of this category are identified.


### 3. GENERAL METHODOLOGY 
- Data collection
- Data Validation
- Insertion into Database, (Here, MySql database is used)
- Exploratory Data Analysis(plotly, matplotlib, seaborn )
- Data preprocessing based on EDA
- Model building(AutoML library pycaret is 
used for model selection, 
random forest is selected as the best model, training is done is 
 google colab due to large dataset)
- Prediction
- Flask api creation
- Deployment(Heroku)

####Data preprocessing tasks done are <br>
- Unwanted and redundant columns are removed
- Certain cumulative features were found to have high corelation,
they are combined to form single feature.
- there were over 6 lac records and only less than 100 unique values,
which is not idel for a regression problem, hence labels were assigned
to form a classification problem
(refer EDA for more info)
- Data was heavily imabalanced . Hence __RandomUndersampling__ was
done and data was reduced to 3 lac records.
- Page category was one hot encoded.

##Project Structure
- main.py : Entry point of the application. API is crated using flask
- requirements.txt: file for replicating virtual env.
- COLAB notebooks : .ipynb file from google colab. Training was done on colab
- Combined_prediction_data: combines multiple prediction batch files
into single file for prediction from the database.
- Combined_training_data: Data extracted from DB for training the model,
can be used for retraining as well.
- DATA_PREPROCESSING : Contains all the classes for data preprocessing,
- DATA_VALIDATION : Contains .py files for validating the prediction
and training files
- DB_OPERATIONS : Contains all classes for database operations of training data and prediction data.
MySql database is used here. 
- Exploratory Data Analysis: .ipynb files containing eda
- LOGS : All the information during runtime is stored in appropriate logs.
logger module is used for logging.
- MODELLING - Contains .py files for creating the model during training/retraing4
- PREDICTION - .py files for prediction
- Prediction_Results : results of prediction
- Raw_Data_Training: Files uploaded by user/client
- templates: .html files for UI
- Training_batches: Training data obtained from database

[Dataset info](https://archive.ics.uci.edu/ml/datasets/Facebook+Comment+Volume+Dataset#)




