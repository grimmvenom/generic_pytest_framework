#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.commonVariables import *
import requests
import re
import urllib
import json
import base64
from datetime import date
from decimal import Decimal
from schema import Schema, And, Use, Optional
from dateutil.parser import parse
from netifaces import AF_INET, AF_INET6, AF_LINK
import netifaces as ni
from allure_commons.types import AttachmentType
from allure_commons.reporter import AllureReporter
import allure_commons
from behave import *
import uuid
import configparser


"""
Author: grimmvenom <grimmvenom@gmail.com>
=====================================================
# Common Methods for Testing
=====================================================

"""


# context.config.userdata
class testConfig:
    def __init__(self):
        self.userdata = dict()


class emptyContext:
    def __init__(self):
        self.config = testConfig()
        self.config.userdata['variables'] = dict()


def setup_fake_context(environment, environment_config_path, browser, remote=False):
    print(f"environment config path: {environment_config_path}")
    environment = environment.lower()
    browser = browser.capitalize()
    
    config = configparser.RawConfigParser()
    config.read(environment_config_path)
    
    context = emptyContext()  # Setup empty context (Fake w/o using behave)
    # print(f"Context: {context.config.userdata}")
    context.config.userdata['browser'] = browser
    context.config.userdata['environment'] = environment
    context.config.userdata['environment_config_path'] = environment_config_path
    
    for key, value in config[environment].items():
        try:
            context.config.userdata['variables'][str(key)] = str(value)
        except:
            print(f"Error parsing key ({key})")
            pass
    
    if remote:
        print("Fake Context Remote Selenium Set")
        context.config.userdata['selenium_remote_url'] = context.config.userdata['variables']['selenium_remote_url']
    # print(f"Context: {context.config.userdata}\n\n")
    return context


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


# Date can be checked by using lambda string: is_date(string) in schema
def schema_comparison(schema, input):
    try:
        schema = eval(f"Schema({schema})")
        schema.validate(input)
        return None
    except Exception as e:
        LOGGER.error(f"Schema Error: {e}")
        return e
    
    
def context_variable_add(context, key, value):
    log_label = 'commonMethods.py:context_variable_add:: '
    LOGGER.info(log_label + f'Adding context variable {key} with value {value}')
    var_collection = context.config.userdata['variables']
    var_collection[key] = value


def context_variable_get(context, key):
    log_label = 'commonMethods.py:context_variable_get:: '
    LOGGER.info(log_label + f'Getting context variable {key}')
    var_collection = context.config.userdata['variables'][key]
    return var_collection


def context_variable_replacement(context, input, root_key=None):
    if root_key:
        root_key = root_key.lstrip('<')
        root_key = root_key.rstrip('>')

    log_label = 'commonMethods.py:context_variable_replacement:: '

    result = str(input)
    # LOGGER.info(f"{log_label} Checking input: {result}")
    if ('<' and '>' in str(input)) or ('{{' and '}}' in str(input)):
        if 'variables' in context.config.userdata.keys():
            if root_key:
                for key, value in context.config.userdata['variables'][root_key].items():
                    if isinstance(value, dict):
                        value = json.dumps(value)
                    #  LOGGER.info(f"Checking variable with root_key {root_key}: {key}")
                    try:
                        if '<' + str(key) + '>' in str(input):
                            result = result.replace('<' + str(key) + '>', str(value))
                            LOGGER.info('<' + str(key) + "> replaced with " + str(value))
                        elif '{{' + str(key) + '}}' in str(input):
                            result = result.replace('{{' + str(key) + '}}', str(value))
                            LOGGER.info('{{' + str(key) + "}} replaced with " + str(value))
                    except Exception as e:
                        LOGGER.error("Issue on Key (" + str(key) + ") -> " + str(e))
                        continue
            else:
                for key, value in context.config.userdata['variables'].items():
                    # LOGGER.info(f"Replace value: {value} Type: {type(value)}")
                    try:
                        if isinstance(value, dict):
                            value = json.dumps(value)
                    except Exception as err:
                        LOGGER.error(f"Value does not appear to be JSON ready: {err}")

                    # LOGGER.info(f"Checking variable with root_key {root_key}: {key}")
                    try:
                        if '<' + str(key) + '>' in str(input):
                            result = result.replace('<' + str(key) + '>', str(value))
                            LOGGER.info('<' + str(key) + "> replaced with " + str(value))
                        elif '{{' + str(key) + '}}' in str(input):
                            result = result.replace('{{' + str(key) + '}}', str(value))
                            LOGGER.info('{{' + str(key) + "}} replaced with " + str(value))
                    except Exception as e:
                        print("Error on Key: " + str(key))
                        print(e)
                        LOGGER.error("Issue on Key (" + str(key) + ") -> " + str(e))
                        continue
    return result


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
        print(f"Error {err}")
        # LOGGER.info(f"Path not found: {path}")


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


def verify_successful_status_code(response_key, response_value):
    response_value = dict(response_value)
    status_code = response_value['status_code']
    url = response_value['url']
    if status_code in http_success_codes:
        LOGGER.info(f"SUCCESS: Status Code {status_code} for URL {url}")
        assert True
    else:
        LOGGER.error(f"FAILURE: Status Code {status_code} for URL {url} not included in {http_success_codes}")
        assert False, f"FAILURE: Status Code {status_code} for URL {url} not included in {http_success_codes}"


def verify_equal_length(method, content, expected_length: int):
    if len(content) == expected_length:
        LOGGER.info(f"{method}: verify_equal_length: SUCCESS: Length matches expected length")
        assert True
    else:
        LOGGER.info(f"Content of Response:\n {content}")
        LOGGER.info(f"Expected Content Length: {expected_length}")
        LOGGER.info(f"Actual Content Length: {len(content)}")
        LOGGER.error(f"{method}:verify_equal_length: FAILURE: Length does not match expected length")
        assert False, f"{method}:verify_equal_length: FAILURE: Length does not match expected length"


def verify_key_as_integer(method, content, key):
    for index, entry in enumerate(content):
        if isinstance(entry['id'], int):
            LOGGER.info(f"{method}:verify_key_integer: SUCCESS: index ({index}): key ({key}): value is an integer")
            assert True
        else:
            LOGGER.error(f"{method}:verify_key_integer: FAILURE: index ({index}): key ({key}): value is NOT an integer")
            assert False, f"{method}:verify_key_integer: FAILURE: index ({index}): key ({key}): value is NOT an integer"


def verify_key_value_no_spaces(method, content, key):
    for index, entry in enumerate(content):
        if ' ' not in entry[key]:
            LOGGER.info(f"{method}:verify_key_value_no_spaces: SUCCESS: index({index}) Value does NOT contain spaces")
            assert True
        else:
            LOGGER.info(f"{entry[key]}: Contains Spaces")
            LOGGER.error(f"{method}:verify_key_value_no_spaces: FAILURE: index({index}) Value does contain spaces")
            assert False, f"{method}:verify_key_value_no_spaces: FAILURE: index({index}) Value does contain spaces"


def environment_check(context, log_label):
    if "environment" in context.config.userdata.keys():
        environment = context.config.userdata["environment"]
    else:
        LOGGER.error(f"{log_label} FAILURE: environment was not set")
        assert False, f"environment was not set"
        
    if "environment_config_path" in context.config.userdata.keys():
        environment_config_path = context.config.userdata["environment_config_path"]
    else:
        LOGGER.error(f"{log_label} FAILURE: Testing environment configuration file not specified")
        assert False, f"Testing environment configuration file not specified"
        
    if "browser" in context.config.userdata.keys():
        browser = context.config.userdata["browser"]
    else:
        LOGGER.error(f"{log_label} FAILURE: browser context was not set")
        assert False, f"browser context was not set"
        
    return environment, environment_config_path, browser
