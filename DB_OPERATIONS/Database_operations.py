import json
import os
import csv
import mysql.connector
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(name)s : %(asctime)s :  %(message)s')
file_handler = logging.FileHandler('LOGS/DB_operation_logs/Db_ops.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class DB_operation:
    """"
    This class contains all methods for performing DataBase operations
    :parameter:None
    """
    def __init__(self,filepath, table_name, output_path):
        try:
            self.filepath = filepath # Directory containing all training batches
            self.table_name = table_name
            self.output_path = output_path
            logger.info("Instance of DB_operation created params: {} , {}, {}".format(self.filepath
                                                                                      , self.table_name, self.output_path))
        except Exception as e:
            logger.error("object initiation failer : {}".format(e))
            raise e

    def db_conn(self, db_name):
        """"
        Description: Return a connection object to the given database , if it exists
                        else, make a new database and return the connection object.

        :parameter: db_name, name of the database
        :returns: conn, connection object to the database
        """
        try:
            try: # if database already exists
                conn = mysql.connector.connect(user='root', password='qwerty12345',
                                               host='127.0.0.1', database=db_name)
                logger.info("{} databse exists!! connection created".format(db_name))


            except: # if database does not exists
                conn = mysql.connector.connect(user='root', password='qwerty12345',
                                               host='127.0.0.1')
                c= conn.cursor()
                c.execute("CREATE DATABASE  {}".format(db_name))
                conn.close()
                conn = mysql.connector.connect(user='root', password='qwerty12345',
                                               host='127.0.0.1', database=db_name)
                logger.info("{} database created, connection established".format(db_name))


            return conn

        except Exception as e:
            logger.error("Failed to establish DB connection: {} ".format(e ))
            raise e


    def create_table(self, conn, col_info):
        """"
        Description: Creates table 'table_name' , if already exists drops the table and create new table.
        :parameter:conn, connection object to database
                   table_name: name of the table
                   col_info: Col info obtained from .json file
        :returns:None
        """
        try:
            c = conn.cursor()
            c.execute("DROP TABLE IF EXISTS {}".format(self.table_name))

            for col_name in col_info.keys():
                try:
                    c.execute("ALTER TABLE {} ADD COLUMN {} {}".format(self.table_name, col_name, col_info[col_name]) )
                except:
                    c.execute("CREATE TABLE {} ({} {})".format(self.table_name, col_name, col_info[col_name]) )
            conn.commit()
            logger.info("Table '{}' Created Successfully".format(self.table_name))

        except Exception as e:
            logger.error("Failed to create table '{}'".format(self.table_name))
            raise e


    def insert_values_to_table(self, conn):
        """"
        Description: This method inserts all the data to the table
        :parameter : Connection Object,
        """
        try:
            c=conn.cursor()
            for file in os.listdir(self.filepath):
                f = open( os.path.join(self.filepath, file), 'r')
                reader = csv.reader(f, delimiter='\n')
                for line in reader:
                    c.execute("INSERT INTO {} VALUES ({})".format(self.table_name, line[0]))
                f.close()
                break
            conn.commit()
            logger.info("Data inserted to table '{}' Successfully".format(self.table_name))

        except Exception as e:
            logger.error("Failed to insert values to table '{}'".format(self.table_name))
            raise e

    def export_csv(self, conn):

        try:
            c = conn.cursor()
            c.execute('SELECT * FROM {}'.format(self.table_name))
            results = c.fetchall()
            headers = [i[0] for i in c.description]
            try:
                csvFile = csv.writer(open(self.output_path, 'w', newline=''), delimiter=',', lineterminator='\r\n',
                                     quoting=csv.QUOTE_ALL, escapechar='\\')
                csvFile.writerow(headers)
                csvFile.writerows(results)
            except:# if directory does not exists
                os.makedirs(self.output_path.split('/')[0])
                csvFile = csv.writer(open(self.output_path, 'w', newline=''), delimiter=',', lineterminator='\r\n',
                                     quoting=csv.QUOTE_ALL, escapechar='\\')
                csvFile.writerow(headers)
                csvFile.writerows(results)
            logger.info("Exported csv file to {}".format(self.output_path))

        except Exception as e:
            logger.error("Failed to insert values to table '{}'".format(self.table_name))
            raise e




    def close_connection(self,conn):
        try:
            conn.close()
            logger.info("Closed db connection ")
            logger.info("DB OPS COMPLETED")

        except Exception as e:
            logger.error("Failed to insert values to table '{}'".format(self.table_name))
            raise e







