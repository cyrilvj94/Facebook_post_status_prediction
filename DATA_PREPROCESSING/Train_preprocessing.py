import pandas as pd
import numpy as np
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
import random
import os
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s :  %(message)s')
file_handler = logging.FileHandler('LOGS/Data_preprocessing_logs/preprocessing_train.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Preprocessing:
    """"
    Description: This class is for handling all the preprocessing related tasks.
    :parameter: Raw validated Data
    """
    label_dic = {0: [0], 1: [1, 2], 2: range(3, 11), 3: range(0, 11)} # Class Variable

    def __init__(self,  file_path, no):
        try:
            self.file_path = file_path
            self.data = pd.read_csv(self.file_path)
            self.label_dic =  {0: [0],1: [1, 2],2: range(3, 11),3: range(0, 11)}
            self.no = no
            logger.info('Instance Created Successfully shape of csv file {}'.format(self.data.shape))
            if self.no == 0 :
                logger.info("Start of data preprocessing - TRAINING ")
            else:
                logger.info("Start of data preprocessing - PREDICTION ")

        except Exception as e:
            logger.error("failed to created instance")
            raise e

    def remove_unwanted_columns(self):
        """"
        Description:Remove umwanted columns from the data
        :parameter: None
        :returns: None
        """
        try:
            cols_to_remove = ['c1_min', 'c1_max', 'c1_avg', 'c1_median', 'c1_std_dev','post_promotion_status',
                              'c2_min', 'c2_max', 'c2_avg', 'c2_median', 'c2_std_dev',
                              'c3_min', 'c3_max', 'c3_avg', 'c3_median', 'c3_std_dev',
                              'c4_min', 'c4_max', 'c4_avg', 'c4_median', 'c4_std_dev',
                              'c5_min', 'c5_max', 'c5_avg', 'c5_median', 'c5_std_dev',
                              'post_pub_sat', 'base_sat', 'c5', 'c4']
            self.data.drop(cols_to_remove, axis = 1, inplace = True)
            logger.info("Unwanted columns removed successfully, shape {}".format(self.data.shape))
        except Exception as e:
            logger.error("Error in attempting column removal")
            raise e

    def combine_comments(self):
        """"
        Description: Combine comments columns since they have high corelation
                   Drops columns c1, c2, c3
        """
        try:
            self.data['c_derived'] = (1.25 * self.data.c1 + 1.5 * self.data.c2 + self.data.c3) / 3
            self.data.drop(['c1', 'c2', 'c3'], axis=1, inplace=True)
            logger.info("Comments combined to form new derived feature")
            logger.info("Dropped c1, c2, c3 columns , shape: {}".format(self.data.shape))

        except Exception as e:
            logger.error("Error in combining comments or removing columns c1, c2,c3,c4")
            raise e

    def label_comments_recieved(self):
        """"
        Description: -->>Labels comments_received feature and transforms it into post_status
                    -->>Drops the feature comments_received
        :parameter: None
        """
        try:
            self.data['post_status'] = self.data.comments_received.apply(self.comm_label_fn)
            self.data.drop('comments_received', axis=1, inplace=True)
            logger.info("Labelled comments_received column")

        except Exception as e:
            logger.error("Error in Labelling comments_received column")
            raise e


    def seperate_features_labels(self):
        """"
        Description: Seperated features and labels
        """
        try:
            self.X = self.data.drop('post_status', axis=1)
            self.y = self.data[['post_status']]
            logger.info("features and labels seperated shapes {} and {}".format(self.X.shape, self.y.shape))

        except Exception as e:
            logger.error("Error in Labelling comments_received column")
            raise e

    def random_undersampling(self):
        """"
        Description: For balancing the data
        """
        try:
            under_sampler = RandomUnderSampler(sampling_strategy={0:87000, 1:87000 , 2:86571 , 3:67950}, random_state=3)
            self.X, self.y = under_sampler.fit_resample(self.X, self.y)
            logger.info("Samples has required counts, shapes : {} , {}".format(self.X.shape, self.y.shape))
        except:
            under_sampler = RandomUnderSampler(random_state=3)
            self.X, self.y = under_sampler.fit_resample(self.X, self.y)
            logger.info("Samples does not have required counts, hence samplling strategy set"
                        " to 'auto' shapes : {} , {}".format(self.X.shape, self.y.shape))



    def encoding_pg_category(self):

        try:
            top_frequent = self.X.pg_category.value_counts().sort_values(ascending=False).iloc[:11].index.to_list()
            a = np.random.choice( list(set(self.X.pg_category.unique() ).difference(top_frequent),) , 1)[0]
              # a should be a no not in top_frequent

            def encoding_fn(x):
                if x in top_frequent:
                    return x
                else:
                    return a
            lst = []
            top_frequent.append(a)
            #print(top_frequent)
            for i in  top_frequent:
                lst.append("col_{}".format(int(i)))
            d = dict( zip(top_frequent, lst))
            #print(d)
            self.X['label_pg_category'] = self.X.pg_category.apply(encoding_fn)  # assigning new categories
            dummies = pd.get_dummies(self.X.label_pg_category, drop_first=False)
            self.X = pd.concat([self.X, dummies], axis=1)
            self.X.drop(['pg_category', 'label_pg_category'], axis=1, inplace=True)
            self.X.rename(columns = d, inplace = True)
            print(self.X.columns)
            self.X.drop(['col_{}'.format(int(a))], axis=1, inplace= True) # updated
            logger.info("Encoded pg_category")
            logger.info("Frequent labels encoded  {} and shape {} {}".format(top_frequent, self.X.shape, self.y.shape))

        except Exception as e:
            logger.error("Error While Encoding pg_category")
            raise e




    @staticmethod
    def comm_label_fn(x):
        """"
            Description: function for pd.apply in self.label_comments_received
            """

        if x in Preprocessing.label_dic[0]:
            return 0
        if x in Preprocessing.label_dic[1]:
            return 1
        if x in Preprocessing.label_dic[2]:
            return 2
        else:
            return 3














