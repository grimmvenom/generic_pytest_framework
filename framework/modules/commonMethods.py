#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import configparser
import json
import re
import urllib
import uuid
from datetime import date
from decimal import Decimal
import psutil
import pytest
import allure_commons
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from dateutil.parser import parse
from framework.modules.assertions import assert_eq_json
from framework.modules.commonVariables import *
import netifaces as ni
from netifaces import AF_INET, AF_INET6, AF_LINK
from schema import And, Optional, Schema, Use


def determine_test_status(self):
    if len(pytest.variables['errors']) >= 1:
        LOGGER.error(f"[ FAILURE ] {pytest.variables['method_name']}: {pytest.variables['errors']}")
        assert False, f"[ FAILURE ]{pytest.variables['method_name']}: {pytest.variables['errors']}"
        return False
    else:
        LOGGER.info(f"[ SUCCESS ]: {pytest.variables['method_name']}")
        assert True
        return True


def validate_status_code(self, expected_status, response):
    if int(response['response_status_code']) != int(expected_status):
        message = f"Expected a {expected_status} Status Code, Got {response['response_status_code']} instead"
        pytest.variables['errors'].append(message)
        LOGGER.error(message)
        

def validate_schema(self, schema_definition, json_response):
    schema_status = schema_comparison(schema_definition, json_response)
    if schema_status != None:
        pytest.variables['errors'].append(f"Issue with json response: {schema_status}")
        LOGGER.error(f"Issue with json response: {schema_status}")


# Date can be checked by using lambda string: is_date(string) in schema
def schema_comparison(schema_definition, input):
    try:
        # schema = eval(f"Schema({schema})")
        schema = Schema(schema_definition)
        schema.validate(input)
        return None
    except Exception as e:
        LOGGER.info(f"Schema: {schema}")
        LOGGER.info(f"JSON: {input}")
        LOGGER.error(f"Schema Error: {e}")
        return e


def validate_response_json_values(self, expected_json, json_response):
    for key, value in expected_json.items():
        try:
            if json_response[key] != value:
                message = f"Expected {key} = ({value}), got ({json_response[key]}) instead"
                pytest.variables['errors'].append(message)
                LOGGER.error(message)
        except KeyError as e:
            message = f"Unable to find Key: {key} in response"
            pytest.variables['errors'].append(message)
            LOGGER.error(message)
            continue


def compare_two_lists(list1: list, list2: list) -> bool:
        res = [i for i in list1 if i not in list2] + [j for j in list2 if j not in list1]
        return res


def get_network_interfaces():
    interfaces = ni.interfaces()
    return interfaces


def get_ip_addresses():
    interfaces = get_network_interfaces()
    ip_addresses = dict()
    for interface in interfaces:
        try:
            address = ni.ifaddresses(interface)[AF_INET][0]['addr']
            ip_addresses[interface] = {'address': str(address)}
        except:
            pass
    return ip_addresses
    
    
def diff_lists(list1, list2):
    list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return list_dif


def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False

    
def get_http_protocol(url):  # Get Protocol of URL
    return re.findall('(?i)(https?:)', url)[0].replace(":", "")


def get_site_root(url):  # Get site root of URL
    parsed_uri = urllib.parse.urlparse(str(url))
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result


def detect_valid_url(string):  # Detect if URL is valid
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if re.match(regex, string) is not None:
        result = True
    else:
        result = "Malformed"
    return result


def get_extension(file: str):  # Get extension of file
    return str(re.findall('(?i)(\.\w{2,4})', file)[-1])


def validate_keys_exist(expected_keys, object):
    keys_not_found = list()
    for key in expected_keys:
        fields_found = search_json_recursively(object, key)
        if not len(fields_found) >= 1:
            keys_not_found.append(key)

    if len(keys_not_found) >= 1:
        pytest.variables['errors'].append(f"Issue finding keys: {keys_not_found} in ({object})")
        LOGGER.error(f"Issue finding keys: {keys_not_found} in ({object})")
    return keys_not_found


def search_json_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.items():

        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = search_json_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = search_json_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found



def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
