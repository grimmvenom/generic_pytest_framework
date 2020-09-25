#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os, json
from conftest import *

TestCase = os.path.basename(__file__)
get_test_data = [("https://reqres.in/api/users")]


# Test GET Responses
class Test_GET_General:
	# Perform Unique Get Requests once so we do not DoS API EndPoint
	get_responses = dict_loop_get_requests(TestCase + ":Test_GET_General", get_test_data)

	@pytest.mark.parametrize("response_key, response_value", get_responses.items())
	def test_success_GET_status_code(self, response_key, response_value):
		verify_successful_status_code(TestCase + ":test_success_GET_status_code", response_key, response_value)
	
	@pytest.mark.parametrize("responses, length", [(get_responses, 6)])
	def test_validate_expected_result_length(self, responses, length):
		for response_key, response_data in responses.items():
			response_data = dict(response_data)
			content = response_data['content']['data']
			verify_equal_length(TestCase + ":test_validate_expected_result_length", content, length)

	@pytest.mark.parametrize("responses, key", [(get_responses, 'id')])
	def test_verify_key_as_integer(self, responses, key):
		for response_key, response_data in responses.items():
			response_data = dict(response_data['content'])
			content = response_data['data']
			verify_key_as_integer(TestCase + ":test_verify_key_as_integer", content, key)

	@pytest.mark.parametrize("responses, key", [(get_responses, 'first_name')])
	def test_verify_first_name_no_spaces(self, responses, key):
		for response_key, response_data in responses.items():
			response_data = dict(response_data['content'])
			verify_key_value_no_spaces(TestCase + ":test_verify_first_name_no_spaces", response_data['data'], key)
	
	@pytest.mark.parametrize("responses, key", [(get_responses, 'last_name')])
	def test_verify_first_name_no_spaces(self, responses, key):
		for response_key, response_data in responses.items():
			response_data = dict(response_data['content'])
			verify_key_value_no_spaces(TestCase + ":test_verify_last_name_no_spaces", response_data['data'], key)
