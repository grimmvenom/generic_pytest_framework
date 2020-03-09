#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resources:
	https://docs.pytest.org/en/latest
	https://docs.qameta.io/allure/
	https://github.com/allure-framework/allure2
	https://github.com/pytest-dev/pytest-html
	
# Test URLs:
	https://reqres.in/
	https://jsonplaceholder.typicode.com/guide.html

# Example Commands:
py.test test_generic_GET.py -vs  # Will run tests and print stdout
	py.test --alluredir=../allure_results
	py.test --alluredir=../allure_results --clean-alluredir -vs test_generic_GET.py  # Will run specific test and print stdout
	py.test test_generic_GET.py -k <method> -s  # Will run specific test + method and print stdout
	py.test -rA <file>   # Will execute test and give a quick summary at the end of stdout
	py.test --html=report.html --self-contained-html ./  # Generate HTML Output
	
	py.test --html=../Logs_PyTest/report.html --self-contained-html --alluredir=../allure_results --clean-alluredir -vs ./
"""

import pytest
import requests
import os
import time
import json
import logging
import allure_pytest

# Global Variables
directories = ["logs", "logs" + os.sep + "pytest_results",  "logs" + os.sep + "allure_results"]
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
date = time.strftime("%m-%d-%Y") # Date Format mm-dd-yyyy_Hour_Min
Time = time.strftime("%H_%M") # Time
report_time = time.strftime("%I_%M_%p")
sys_time = time.strftime("%I_%M_%p")

http_success_codes = [200, 201, 202, 301, 302]

LOGGER = logging.getLogger(__name__)

# Setup / Configuration of local directories
for directory in directories:
	if not os.path.exists(current_dir + os.sep + directory):
		os.makedirs(current_dir + os.sep + directory)

"""
=====================================================
# Common Methods for Testing
=====================================================
"""


def dict_loop_get_requests(method, inventory):
	get_responses = dict()
	for item in enumerate(inventory):
		index = str(item[0])
		url = str(item[1])
		content, status_code, headers = http_get_request_json(method + ":dict_loop_get_requests", url)
		get_responses[index] = {'url': str(url), 'content': dict(content), 'status_code': int(status_code), 'headers': dict(headers)}
	# print(json.dumps(dict(get_responses), indent=4, sort_keys=False))
	return get_responses


def dict_loop_post_requests(method, inventory):
	post_responses = dict()
	for index, item in enumerate(inventory):
		url = str(item[0])
		data = str(item[1])
		content, status_code, headers = http_post_request_json(method + ":dict_loop_post_requests", url, data)
		post_responses[index] = {'url': str(url), 'content': dict(content), 'status_code': int(status_code), 'headers': dict(headers), 'data_sent': data}
	# print(json.dumps(dict(get_responses), indent=4, sort_keys=False))
	return post_responses


def http_get_request_json(method, url):
	print("\nGetting URL: ", url)
	results = requests.get(url)
	content = results.json()
	status_code = results.status_code
	headers = results.headers
	LOGGER.info(method + ":http_get_request_json: Requesting: " + str(url) + " Status Code: " + str(status_code))
	return content, status_code, headers


def http_post_request_json(method, url, data):
	print("\nPOSTing to URL: ", url)
	results = requests.post(url, data=data)
	content = results.json()
	status_code = results.status_code
	headers = results.headers
	LOGGER.info(method + ":http_post_request_json: POSTing Data: " + str(url) + " Status Code: " + str(status_code))
	return content, status_code, headers


def verify_successful_status_code(TestCase, response_key, response_value):
	response_value = dict(response_value)
	status_code = response_value['status_code']
	url = response_value['url']
	if status_code in http_success_codes:
		LOGGER.info(str(TestCase) + ":verify_successful_status_code: SUCCESS: Status Code " + str(status_code) + " for URL " + url)
		assert True
	else:
		LOGGER.error(str(TestCase) + ":verify_successful_status_code: FAILURE: Status Code " + str(status_code) + " for URL " + url + " not included in " + str(http_success_codes))
		assert False


def verify_equal_length(method, content, expected_length: int):
	if len(content) == expected_length:
		LOGGER.info(method + ":verify_equal_length: SUCCESS: Length matches expected length")
		assert True
	else:
		LOGGER.error(method + ":verify_equal_length: FAILURE: Length does not match expected length")
		LOGGER.info("Content of Response:\n " + str(content))
		LOGGER.info("Expected Content Length: " + str(expected_length))
		LOGGER.info("Actual Content Length: " + str(len(content)))
		assert False


def verify_key_as_integer(method, content, key):
	for index, entry in enumerate(content):
		if isinstance(entry['id'], int):
			LOGGER.info(method + ":verify_key_integer: SUCCESS: index (" + str(index) + "): key (" + str(key) + "): value is an integer")
			assert True
		else:
			print("FAILED Entry: ")
			print(entry)
			LOGGER.error(method + ":verify_key_integer: FAILURE: index (" + str(index) + "): key (" + str(key) + "): value is NOT an integer")
			assert False


def verify_key_value_no_spaces(method, content, key):
	for index, entry in enumerate(content):
		if ' ' not in entry[key]:
			LOGGER.info(method + ":verify_key_value_no_spaces: SUCCESS: index(" + str(index) + ") Value does NOT contain spaces")
			assert True
		else:
			LOGGER.error(method + ":verify_key_value_no_spaces: FAILURE: index(" + str(index) + ") Value does contain spaces")
			LOGGER.info(str(entry[key]) + " : Contains Spaces")
			assert False
