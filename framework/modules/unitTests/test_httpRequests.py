#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../../'))
import pytest
from framework.modules.httpRequests import *

TestCase = os.path.basename(__file__)


# Test httpRequests.py methods
class Test_httpRequests:
    
    def test_http_get_request_success(self):
        url = "https://postman-echo.com/get/"
        api_request = ApiRequest("get", url, json_payload={}, data={}, headers={})
        results = api_request.perform_request()
        if int(results["response_status_code"]) in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: GET request to {url}")
            assert True
        else:
            LOGGER.error(f"[ ERROR ]: GET request to {url}: expected any({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: GET request to {url}: expected any({http_success_codes}), but got status code {results['response_status_code']} instead"

    def test_http_get_request_failure(self):
        url = "https://postman-echo.com/get/test"
        api_request = ApiRequest("get", url, json_payload={}, data={}, headers={})
        results = api_request.perform_request()
        if int(results["response_status_code"]) not in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: GET request to {url} failed as expected")
            assert True
        else:
            LOGGER.error(f"[ ERROR ]: GET request to {url}: expected anything except: ({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: GET request to {url}: expected anything except:({http_success_codes}), but got status code {results['response_status_code']} instead"

    def test_http_post_request_with_payload_success(self):
        url = "https://reqbin.com/echo/post/json"
        api_request = ApiRequest("post", url, data={}, json_payload={"jsonKey": "jsonValue"}, headers={"headerKey": "headerValue"})
        results = api_request.perform_request()
        if int(results["response_status_code"]) in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: POST request to {url}")
            assert True
        else:
            LOGGER.error(
                f"[ ERROR ]: POST request to {url}: expected({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: POST request to {url}: expected({http_success_codes}), but got status code {results['response_status_code']} instead"

    def test_http_post_request_with_payload_failure(self):
        url = "https://postman-echo.com/post/fail"
        api_request = ApiRequest("post", url, data={}, json_payload={"jsonKey": "jsonValue"}, headers={"headerKey": "headerValue"})
        results = api_request.perform_request()
        if int(results["response_status_code"]) not in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: POST request to {url} failed as expected")
            assert True
        else:
            LOGGER.error(
                f"[ ERROR ]: POST request to {url}: expected anything except: ({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: POST request to {url}: expected anything except: ({http_success_codes}), but got status code {results['response_status_code']} instead"
    
    def test_http_put_request_with_payload_success(self):
        url = "https://reqbin.com/echo/put/json"
        api_request = ApiRequest("put", url, data={}, json_payload={"jsonKey": "jsonValue"}, headers={"headerKey": "headerValue"})
        results = api_request.perform_request()
        if int(results["response_status_code"]) in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: PUT request to {url}")
            assert True
        else:
            LOGGER.error(
                f"[ ERROR ]: PUT request to {url}: expected({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: PUT request to {url}: expected({http_success_codes}), but got status code {results['response_status_code']} instead"

    def test_http_put_request_with_payload_failure(self):
        url = "https://postman-echo.com/put/fail"
        api_request = ApiRequest("put", url, data={}, json_payload={"jsonKey": "jsonValue"}, headers={"headerKey": "headerValue"})
        results = api_request.perform_request()
        if int(results["response_status_code"]) not in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: PUT request to {url} failed as expected")
            assert True
        else:
            LOGGER.error(
                f"[ ERROR ]: PUT request to {url}: expected anything except: ({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: PUT request to {url}: expected anything except: ({http_success_codes}), but got status code {results['response_status_code']} instead"

    def test_http_delete_request_with_payload_success(self):
        url = "https://reqbin.com/echo/delete/json"
        api_request = ApiRequest("delete", url, data={}, json_payload={"jsonKey": "jsonValue"}, headers={"headerKey": "headerValue"})
        results = api_request.perform_request()
        if int(results["response_status_code"]) in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: DELETE request to {url}")
            assert True
        else:
            LOGGER.error(
                f"[ ERROR ]: DELETE request to {url}: expected({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: DELETE request to {url}: expected({http_success_codes}), but got status code {results['response_status_code']} instead"

    def test_http_delete_request_with_payload_failure(self):
        url = "https://postman-echo.com/delete/fail"
        api_request = ApiRequest("delete", url, dict(), {"jsonKey": "jsonValue"}, {"headerKey": "headerValue"})
        results = api_request.perform_request()
        if int(results["response_status_code"]) not in http_success_codes:
            LOGGER.info(f"[ SUCCESS ]: DELETE request to {url} failed as expected")
            assert True
        else:
            LOGGER.error(
                f"[ ERROR ]: DELETE request to {url}: expected anything except: ({http_success_codes}), but got status code {results['response_status_code']} instead")
            assert False, f"[ ERROR ]: DELETE request to {url}: expected anything except: ({http_success_codes}), but got status code {results['response_status_code']} instead"
    
    def test_http_verify_response_content(self):
        url = "https://reqbin.com/echo/post/json"
        api_request = ApiRequest("post", url, data={}, json_payload={"jsonKey": "jsonValue"}, headers={"headerKey": "headerValue"})
        results = api_request.perform_request()
        if 'response_content' in results.keys() and len(results['response_content']) >= 1:
            LOGGER.info(f"[ SUCCESS ]: response content is returned {results['response_content']}")
            assert True
        else:
            LOGGER.error(f"[ ERROR ]: response content not returned -> result keys ({results.keys()})")
            assert False, f"[ ERROR ]: response content not returned -> result keys ({results.keys()})"
            
    def test_http_verify_response_headers(self):
        url = "https://reqbin.com/echo/post/json"
        api_request = ApiRequest("post", url, data={}, json_payload={"jsonKey": "jsonValue"}, headers={"headerKey": "headerValue"})
        results = api_request.perform_request()
        if 'response_header' in results.keys() and len(results['response_header']) >= 1:
            LOGGER.info(f"[ SUCCESS ]: response headers are returned {results['response_header']}")
            assert True
        else:
            LOGGER.error(f"[ ERROR ]: response headers not returned -> result keys ({results.keys()})")
            assert False, f"[ ERROR ]: response headers not returned -> result keys ({results.keys()})"
