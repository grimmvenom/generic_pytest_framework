#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('../../../')
from framework.modules.commonMethods import *
from framework.modules.commonVariables import *
import os, sys, time
import json
from datetime import date
import mysql.connector
from mysql.connector import Error


def db_load_from_file(self, path):
    try:
        os.path.isfile(path)
        content_array = []
        with open(path) as f:
            for line in f:
                content_array.append(line)

        for line in content_array:
            try:
                # print(f'{line}')
                self.cursor.execute(line)
            except Exception as err:
                print(f"- SQL Statement Error: Line # {line} - {err}")
                LOGGER.error(f"SQL Error: Line# {line} - {err}")

        self.connection.commit()

    except Exception as err:
        LOGGER.error(f"{err} - Path not found: {path}")


def db_setup(environment, environment_config_path, context=None):
    # env_path = parent_parent + os.sep + 'config.ini'
    if context:
        LOGGER.info(f"Context environment set to: {environment}")
        if 'db' not in context.config.userdata.keys():
            context.config.userdata['db'] = dict()
    
    db_config = dict()
    config = configparser.RawConfigParser()
    config.read(environment_config_path)
    try:
        db_config["environment"] = environment
        db_config['db_name'] = str(config[environment]['db_name'])
        db_config['db_type'] = str(config[environment]['db_type'])
        db_config['db_username'] = str(config[environment]['db_username'])
        db_config['db_password'] = str(config[environment]['db_password'])
        db_config['db_host'] = str(config[environment]['db_host'])
        db_config['db_port'] = str(config[environment]['db_port'])
        LOGGER.info(f"dbConfig: {db_config}")
        if context:
            try:
                for key, value in db_config.items():
                    context.config.userdata["db"][str(key)] = str(value)
            except Exception as e:
                LOGGER.warning(f"DB Setup issue w/ context {e}")
                pass
        return db_config
    except Exception as e:
        LOGGER.error(f" [ ERROR ]: {e}")
        assert False, f"Error setting DB Environment: {e}"


def db_results_to_dict(results):
    result_list = []
    for row in results:
        result_list.append(dict(row))
    
    result_json = json.dumps(result_list, cls=DBEncoder)
    result_json = json.loads(result_json)
    LOGGER.info(f"DB Query Results: {result_json}")
    return result_json


class DBEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float("{0:.2f}".format(obj))
            # return float("{0:.2f}".format(Decimal(obj)))
            # return str(Decimal(obj))
        return json.JSONEncoder.default(self, obj)


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
        if self.db_type == "mysql":
            results = self.query_mysql(str(query))
            return results
        else:
            LOGGER.error(f"DB Type not Supported")
            return "DB TYPE not supported"
    
    def query_mysql(self, query):
        query_start_time = time.time()
        LOGGER.info(f"Query: {query}")
        try:
            connection = mysql.connector.connect(host=str(self.db_host),
                                            port=int(self.db_port),
                                            database=str(self.db_name),
                                            user=str(self.db_username),
                                            password=str(self.db_password))
            cursor = connection.cursor()

            if any(substring in query for substring in ["update", "UPDATE", "delete", "DELETE"]):
                LOGGER.info(f"query is of TYPE (update / delete): {query}")
                cursor.execute(query)
                connection.commit()
                LOGGER.info(f"{cursor.rowcount} record(s) affected")
                return [f"{cursor.rowcount} record(s) affected"]
            else:
                cursor.execute(query)
                column_names = [i[0] for i in cursor.description]
                records = cursor.fetchall()

                updated_records = list()
                for record in records:
                    data = dict()
                    for index, item in enumerate(record):
                        data[column_names[index]] = item
                    updated_records.append(data)
                # Added 03/16
                result_json = json.dumps(updated_records, cls=DBEncoder)
                result_json = json.loads(result_json) # end of added
                end_time = time.time() - query_start_time
                duration = format(end_time / 60, '.2f')
                LOGGER.info(f"mysql DB Query Execution time: {duration} min")
                LOGGER.info(f"[ SUCCESS ]: Query ({query}) returned results: {result_json}")
                return result_json
            
        except Exception as e:
            LOGGER.error(f"[ Error ] connecting to mysql DB: {e}")
