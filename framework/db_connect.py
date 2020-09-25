#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Author: nick serra <nserra@riis.com>

Summary:
    To perform various database queries based on input of config.ini file

"""
import sys
sys.path.append('../../../')
from framework.commonMethods import *
from framework.commonVariables import *
import os, sys, time
import json
import psycopg2
import psycopg2.extras
import ibm_db
from datetime import date


class DBEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float("{0:.2f}".format(obj))
            # return float("{0:.2f}".format(Decimal(obj)))
            # return str(Decimal(obj))
        return json.JSONEncoder.default(self, obj)


def db_results_to_dict(results):
    # print("Results: ")
    # print(results)
    # print("\n\n")
    result_list = []
    for row in results:
        result_list.append(dict(row))
    
    result_json = json.dumps(result_list, cls=DBEncoder)
    result_json = json.loads(result_json)
    LOGGER.info(f"DB Query Results: {result_json}")
    return result_json


class dbConnect:
    def __init__(self, db_config: dict):
        self.db = None
        # self.cursor.close()
        # self.connection.close()
        self.db_host = db_config['db_host']
        self.db_port = db_config['db_port']
        self.db_name = db_config['db_name']
        self.db_type = db_config['db_type']
        self.db_username = db_config['db_username']
        self.db_password = db_config['db_password']
    
    def query_db(self, query):
        if self.db_type == "h2":
            results = self.query_h2(str(query))
            return results
        elif self.db_type == "db2":
            results = self.query_db2(str(query))
            return results
        else:
            LOGGER.error(f"DB Type not Supported")
            return "DB TYPE not supported"
    
    def query_h2(self, query):
        query_start_time = time.time()
        connection_string = 'dbname=' + str(self.db_name) + \
                            " user=" + str(self.db_username) + \
                            " password=" + str(self.db_password) + \
                            " host=" + str(self.db_host) + \
                            " port=" + str(self.db_port)
        try:
            self.connection = psycopg2.connect(connection_string)
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            end_time = time.time() - query_start_time
            duration = format(end_time / 60, '.2f')
            LOGGER.info(f"H2 DB Query Execution time: {duration} min")
            # print(f'H2 connected at path: {url}\n')
        except Exception as err:
            LOGGER.error(f"[ Error ] connecting to h2 DB: {err}")
        
        try:
            self.cursor.execute(str(query))
            results = self.cursor.fetchall()
            results_json = db_results_to_dict(results)
            return results_json
            # return self.results_to_dict(self.cursor.fetchall())
        except Exception as err:
            LOGGER.error(f"[ Error ] Executing Query ({query}) -> {err}")

    def query_db2(self, query):
        query_start_time = time.time()
        
        connection_string = f'DATABASE={self.db_name};HOSTNAME={self.db_host};PORT={self.db_port};PROTOCOL=TCPIP;UID={self.db_username};PWD={self.db_password};'
        
        try:
            self.connection = ibm_db.connect(connection_string, '', '')

            end_time = time.time() - query_start_time
            duration = format(end_time / 60, '.2f')
            LOGGER.info(f"DB2 Query Execution time: {duration} min")
            # self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # print(f'H2 connected at path: {url}\n')
        except Exception as err:
            LOGGER.error(f"[ Error ] connecting to db2 db: {err}")
        
        try:
            stmt = ibm_db.exec_immediate(self.connection, str(query))
            result_list = []
            try:
                result = ibm_db.fetch_assoc(stmt)
                while result:
                    result_list.append(result)
                    result = ibm_db.fetch_assoc(stmt)
            except Exception as err:
                LOGGER.warn(f"No Results returned from query")
            data = db_results_to_dict(result_list)
            # data = clean_result(data)
            return data
        except Exception as err:
            LOGGER.error(f"[ Error ] Executing Query ({query}) -> {err}")


