#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../../'))
import pytest
from framework.modules.httpRequests import *

TestCase = os.path.basename(__file__)


class Test_API_Demo:

    @classmethod
    def setup_class(self) :  # Setup Method to run before all class tests
        pass

    @classmethod
    def teardown_class(self):  # Teardown Method to run after all class tests are complete
        pass

    def setup_method(self, method):  # Setup method to run at start of each test method
        pytest.variables['method_name'] = f"{method.__name__}"
        pytest.variables['errors'] = list()

    def teardown_method(self, method):
        pass


    def test_http_get_request_success(self):
        url = f"{pytest.variables['base_url']}/get/"
        api_request = ApiRequest("get", url, json_payload={}, data={}, headers={})
        results = api_request.perform_request()
        if int(results["response_status_code"]) in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: GET request to {url}")
            assert True
        else:
            LOGGER.error(f"[ ERROR ]: GET request to {url}: expected any({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: GET request to {url}: expected any({http_success_codes}), but got status code {results['response_status_code']} instead"

    def test_http_get_request_failure(self):
        url = f"{pytest.variables['base_url']}/get/test"
        api_request = ApiRequest("get", url, json_payload={}, data={}, headers={})
        results = api_request.perform_request()
        if int(results["response_status_code"]) not in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: GET request to {url} failed as expected")
            assert True
        else:
            LOGGER.error(f"[ ERROR ]: GET request to {url}: expected anything except: ({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: GET request to {url}: expected anything except:({http_success_codes}), but got status code {results['response_status_code']} instead"
