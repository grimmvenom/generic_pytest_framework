#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath('./'))
import pytest
from framework.commonMethods import *
from framework.httpRequests import *

TestCase = os.path.basename(__file__)


# Test GET Responses
class Test_get_requests:
    
    def test_get_network(self):
        interfaces = get_network_interfaces()
        LOGGER.info(f"test_get_request.py:test_get_network:: Interfaces: {interfaces}")
        assert True
        
    def test_api_get_request(self):
        url = "https://reqres.in/api/users"
        api_request = ApiRequest("get", url, dict(), dict(), dict())
        results = api_request.perform_request()
        if results["response_status_code"] in http_success_codes:
            LOGGER.info(f"GET request to {url}: SUCCESS")
            assert True
        else:
            LOGGER.error(f"GET request to {url}: FAILURE: got status code {results['response_status_code']} instead")
            assert False, f"GET request to {url}: FAILURE: got status code {results['response_status_code']} instead"
    
    # @pytest.mark.parametrize("response_key, response_content", post_responses.items())
