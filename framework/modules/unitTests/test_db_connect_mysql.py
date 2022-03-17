#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../../'))
import pytest
from framework.modules.db_connect import *
from framework.modules.db_connect import *
import configparser
from mysql.connector import Error
from .conftest import *


class Test_db_connect_mysql:
    
    pytest.variables = dict()
    
    # import config.ini variables
    config = configparser.RawConfigParser()
    config.read(config_path)
    for key, value in config[env].items():
        try:
            pytest.variables[str(key)] = str(value)
            LOGGER.info(f"Key ({key}) == {value}")
        except:
            LOGGER.error(str(key))
            pass

    def test_log(self):
        LOGGER.info(f"Config Path: {config_path}")
    

    def test_verify_config(self):
        label = f"db_connect.py: verify_config::"
        if os.path.exists(config_path):
            LOGGER.info(f"[ SUCCESS ]: {label} config file found {config_path}")
            assert True
        else:
            LOGGER.info(f"[ FAILURE ]: {label} config file NOT found {config_path}")
            assert False, f"Config Path not Found: {config_path}"
    

    def test_db_setup(self):
        label = f"db_connect.py: db_setup::"
        if not os.path.exists(config_path):
            LOGGER.info(f"[ FAILURE ]: {label} config file NOT found {config_path}")
            assert False, f"Config Path not Found: {config_path}"
        
        pytest.variables["context"] = setup_fake_context(env, config_path, "Chrome")  # Emulate Fake BDD context
        pytest.variables['db_config'] = db_setup(env, config_path, pytest.variables["context"])
        expected_keys = ["environment", "db_name", "db_type", "db_username", "db_password", "db_host", "db_port"]
        
        if all(key in expected_keys for key in pytest.variables['db_config'].keys()):
            assert True
        else:
            assert False, f"Expected keys({expected_keys}) not found in db_config({pytest.variables['db_config'].keys()})"
        
    def test_show_tables_mysql(self):
        label = f"db_connect.py: dbConnect: mysql: show_tables_mysql:"
        db_config = pytest.variables['db_config']
        db = dbConnect(db_config)
        query = f"show tables from {pytest.variables['db_name']};"
        db_results = db.query_db(str(query))

        if len(db_results) >= 1:
            LOGGER.info(f"[ SUCCESS ]: {label} Query returned expected results: {db_results}")
            assert True
        else:
            LOGGER.error(f"[ FAILURE ]: {label} Query did not return the expected results: {db_results}")
            LOGGER.warnining(f"DB Query may require a VPN connection")
            assert False, f"Query did not return the expected results: {db_results}"

    def test_db_connect_mysql(self):
        label = f"db_connect.py: dbConnect: mysql: query_mysql:"
        db_config = pytest.variables['db_config']
        db = dbConnect(db_config)
        query = f"Select * from {pytest.variables['db_name']}.COUNTRY where COUNTRY_CODE = 'US';"
        db_results = db.query_db(str(query))
        
        if len(db_results) >= 1 and db_results[0]['COUNTRY_NAME'] == "United States":
            LOGGER.info(f"[ SUCCESS ]: {label} Query returned expected results: {db_results}")
            assert True
        else:
            LOGGER.error(f"[ FAILURE ]: {label} Query did not return the expected results: {db_results}")
            LOGGER.warnining(f"DB Query may require a VPN connection")
            assert False, f"Query did not return the expected results: {db_results}"

    def test_db_connect_query_with_date_mysql(self):
        label = f"db_connect.py: dbConnect: mysql: query_with date:"
        db_config = pytest.variables['db_config']
        db = dbConnect(db_config)
        query = f"Select * from {pytest.variables['db_name']}.ACCOUNT LIMIT 1;"
        # query = f"Select * from {pytest.variables['db_name']}.DEVICE_CONFIGURATION where DEVICE_CONFIG_NAME = 'WASHER_WTW617181_DP_A'"
        db_results = db.query_db(str(query))
        
        if len(db_results) >= 1:
            LOGGER.info(f"[ SUCCESS ]: {label} Query returned expected results: {db_results}")
            assert True
        else:
            LOGGER.error(f"[ FAILURE ]: {label} Query did not return the expected results: {db_results}")
            LOGGER.warnining(f"DB Query may require a VPN connection")
            assert False, f"Query did not return the expected results: {db_results}"


    def update_mysql_credentials(self):
        # query = "select * from BLUADMIN.DEVICE_CONFIGURATION where DEVICE_CONFIG_NAME = 'WASHER_WTW617181_DP_A'"
        query = "update BLUADMIN.INBOUND_INVENTORY set ESTIMATED_DELIVERY_DATE = CURDATE() - 1 where INBOUND_INVENTORY_ID = 198;"
        db_config = pytest.variables['db_config']
        db = dbConnect(db_config)
        db_results = db.query_db(str(query))
        print(f"\n\nQuery Results: {db_results}")
        if len(db_results) >= 1:
            LOGGER.info(f"[ SUCCESS ]: update Test: Query returned expected results: {db_results}")
            assert True
        else:
            LOGGER.error(f"[ FAILURE ]: update Test: Query did not return the expected results: {db_results}")
            LOGGER.warnining(f"DB Query may require a VPN connection")
            assert False, f"Query did not return the expected results: {db_results}"


