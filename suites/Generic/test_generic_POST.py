#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os, json
from conftest import *

TestCase = os.path.basename(__file__)
post_test_data = [("https://reqres.in/api/users", '{"name": "tester", "job": "QA Testing"}')]


# Test POST responses
class Test_POST_General:
	# Perform Unique POST Requests once so we do not DoS API EndPoint
	post_responses = dict_loop_post_requests(TestCase + ":Test_POST_General", post_test_data)
	
	@pytest.mark.parametrize("response_key, response_data", post_responses.items())
	def test_success_POST_status_code(self, response_key, response_data):
		verify_successful_status_code(TestCase + ":test_success_POST_status_code", response_key, response_data)
	
	@pytest.mark.parametrize("response_key, response_content", post_responses.items())
	def test_account_creation(self, response_key, response_content):
		response_content = dict(response_content['content'])
		if type(response_content['id']) != int:
			LOGGER.info(TestCase + ":test_account_creation: SUCCESS: id is being returned as an integer")
			assert True
		else:
			LOGGER.error(TestCase + ":test_account_creation: FAILURE: id is NOT being returned as an integer")
			LOGGER.info("id is being returned as: " + str(type(response_content['id'])))
			assert False

