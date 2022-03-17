#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../../..'))
import pytest
from framework.modules.httpRequests import *

TestCase = os.path.basename(__file__)


# Test commonMethods.py methods
class Test_commonMethods:

    def test_get_network(self):
        interfaces = get_network_interfaces()
        if len(interfaces) >= 1:
            LOGGER.info(f"commonMethods.py:get_network_interfaces:: Network Interfaces: {interfaces}")
            assert True
        else:
            LOGGER.error("[ ERROR ]: No network interfaces returned")
            assert False, f"[ ERROR ]: No network interfaces returned"
            
    def test_get_ip_addresses(self):
        ip_addresses = get_ip_addresses()
        if len(ip_addresses.keys()) >= 1:
            LOGGER.info(f"[ SUCCESS ]:commonMethods.py:get_ip_addresses::IP Addresses: {ip_addresses}")
            assert True
        else:
            LOGGER.error(f"[ ERROR ]:commonMethods.py:get_ip_addresses:: No IP Addresses Returned")
            assert False, f"[ ERROR ]:: No IP Addresses Returned"

    def test_diff_lists(self):
        label = "commonMethods: list_diff::"
        list1 = [1, 2, 3, "banana", "apple"]
        list2 = [2, 4, 5, "banana", "lemon"]
        list_diff = diff_lists(list1, list2)
        expected_diff = [1, 3, 'apple', 4, 5, 'lemon']
        if list_diff == expected_diff:
            LOGGER.info(f"[ SUCCESS ]: {label} Got the expected List Diff {list_diff}")
            assert True
        else:
            LOGGER.info(f"[ FAILURE ]: {label} Did not get the expected List ({expected_diff}), got ({list_diff}) instead")
            assert False, f"[ FAILURE ]: {label} Did not get the expected List ({expected_diff}), got ({list_diff}) instead"
            
    def test_is_date(self):
        label = "commonMethods: is_date::"
        statuses = list()
        validations = [{'10/20/2020': True},
                       {'10/20': True},
                       {'October 3rd': True},
                       {'burrito': False}]
        errors = list()
        for check in validations:
            key = list(check.keys())[0]
            value = check[key]
            result = is_date(key)
            if bool(result) == bool(value):
                statuses.append(True)
            else:
                statuses.append(False)
                errors.append(check)
        
        if False in statuses:
            LOGGER.error(f"[ FAILURE ]: {label} is_date returned unexpected value with the following {errors}")
            assert False, f"is_date returned unexpected value with the following {errors}"
        else:
            LOGGER.info(f"[ SUCCESS ]: {label} is_date returned all of the expected results")
            assert True
            
    def test_schema_comparison_valid(self):
        label = "commonMethods: schema_comparison::"
        errors = list()
        json = {"key1": "value1",
                "key2": 217,
                "date": "12/20/2021"}
        schema_design = '{ "key1": str,"key2": int,"date": lambda string: is_date(string) }'
        if schema_comparison(schema_design, json) is not None:
            errors.append(schema_comparison(schema_design, json))
            LOGGER.error(f"[ FAILURE ]: {label} encountered the following schema errors: {errors}")
            assert False, f"json({json}) encountered the following schema errors: {errors}"
        else:
            assert True

    def test_schema_comparison_invalid(self):
        label = "commonMethods: schema_comparison::"
        errors = list()
        schema_design = '{ "key1": str, "key2": int, "date": lambda string: is_date(string) }'
        incorrect_json = {"key1": 18, "key2": 217, "date": "12/20/2020"}
        if schema_comparison(schema_design, incorrect_json) is None:
            errors.append(schema_comparison(schema_design, incorrect_json))
        incorrect_json = {"key1": "value1", "key2": "217", "date": "12/20/2020"}
        if schema_comparison(schema_design, incorrect_json) is None:
            errors.append(schema_comparison(schema_design, incorrect_json))
        incorrect_json = {"key1": "value1", "key2": 217, "date": "burrito"}
        if schema_comparison(schema_design, incorrect_json) is None:
            errors.append(schema_comparison(schema_design, incorrect_json))
        
        if len(errors) >= 1:
            LOGGER.error(f"[ FAILURE ]: {label} encountered the following schema errors: {errors}")
            assert False, f"json({json}) encountered the following schema errors: {errors}"
        else:
            assert True
    
    def test_get_http_protocol(self):
        label = "commonMethods: get_http_protocol::"
        urls = ['https://www.duckduckgo.com', 'http://www.google.com']
        data = dict()
        for url in urls:
            protocol = get_http_protocol(url)
            data[url] = protocol
        
        expected_results = {'https://www.duckduckgo.com': 'https', 'http://www.google.com': 'http'}
        if data != expected_results:
            assert False, f"[ FAILURE ]: {label} data ({data}) != {expected_results}"
        else:
            assert True
    
    def test_get_site_root(self):
        label = "commonMethods: get_site_root::"
        urls = ['https://duckduckgo.com/?q=test&t=h_&ia=web',
                'https://www.google.com/search?source=hp&ei=kFYQYMz1AYb5tAb75YuIDg&q=test&oq=test',
                'http://localhost:80']
        data = dict()
        expected_results = {'https://duckduckgo.com/?q=test&t=h_&ia=web': 'https://duckduckgo.com/',
                            'https://www.google.com/search?source=hp&ei=kFYQYMz1AYb5tAb75YuIDg&q=test&oq=test': 'https://www.google.com/',
                            'http://localhost:80': 'http://localhost:80/'}

        for url in urls:
            site_root = get_site_root(url)
            data[url] = site_root
        if data != expected_results:
            LOGGER.error(f"[ FAILURE ]: {label} data ({data}) does not match expected results ({expected_results})")
            assert False, f"data ({data}) does not match expected results ({expected_results})"
        else:
            assert True
            
    def test_detect_valid_url(self):
        label = "commonMethods: detect_valid_url::"
        urls = ['https://www.duckduckgo.com',
                'http://www.google.com',
                'http://localhost:8675',
                'http://www.example.com/space%20here.html',
                'http://www.example.com/space here.html',
                'http://www.example.com/space&here.html',
                'test.io',
                'ftp://somepath.com']
        data = dict()
        expected_results = {'https://www.duckduckgo.com': True,
                            'http://www.google.com': True,
                            'http://localhost:8675': True,
                            'http://www.example.com/space%20here.html': True,
                            'http://www.example.com/space here.html': 'Malformed',
                            'http://www.example.com/space&here.html': True,
                            'test.io': 'Malformed',
                            'ftp://somepath.com': True}

        for url in urls:
            result = detect_valid_url(url)
            data[url] = result
        
        if data != expected_results:
            LOGGER.error(f"[ FAILURE ]: {label} data ({data}) does not match expected results ({expected_results})")
            assert False, f"data ({data}) does not match expected results ({expected_results})"
        else:
            assert True
    
    def test_get_extension(self):
        label = "commonMethods: get_extension::"
        extensions = ['.pdf', '.img', '.doc', '.docx', '.csv', '.jpg', '.png']
        file_extensions = list()
        for extension in extensions:
            file_extension = get_extension(f"test{extension}")
            file_extensions.append(file_extension)
        if file_extensions != extensions:
            LOGGER.error(f"[ FAILURE ]: {label} extension ({file_extensions}) does not match expected results ({extensions})")
            assert False, f"extension ({file_extensions}) does not match expected results ({extensions})"
        else:
            assert True
            
    def test_search_json_recursively_success(self):
        label = "commonMethods: search_json_recursively::"
        key = "batter"
        json_data = { "id": "0001",
                "type": "donut",
                "name": "Cake",
                "ppu": 0.55,
                "batters":
                    {
                        "batter":
                            [
                                { "id": "1001", "type": "Regular" },
                                { "id": "1002", "type": "Chocolate" },
                                { "id": "1003", "type": "Blueberry" },
                                { "id": "1004", "type": "Devil's Food" }
                            ]
                    },
                "topping":
                    [
                        { "id": "5001", "type": "None" },
                        { "id": "5002", "type": "Glazed" },
                        { "id": "5005", "type": "Sugar" },
                        { "id": "5007", "type": "Powdered Sugar" },
                        { "id": "5006", "type": "Chocolate with Sprinkles" },
                        { "id": "5003", "type": "Chocolate" },
                        { "id": "5004", "type": "Maple" }
                    ]
        }
        results = search_json_recursively(json_data, key)
        if len(results[0]) >= 1:
            assert True
        else:
            LOGGER.error(f"[ FAILURE ]: {label} did not find key ({key}) in json ({json_data})")
            assert False, f"did not find key ({key}) in json ({json_data})"
        
    def test_search_json_recursively_failure(self):
        label = "commonMethods: search_json_recursively::"
        key = "burrito"
        json_data = { "id": "0001",
                "type": "donut",
                "name": "Cake",
                "ppu": 0.55,
                "batters":
                    {
                        "batter":
                            [
                                { "id": "1001", "type": "Regular" },
                                { "id": "1002", "type": "Chocolate" },
                                { "id": "1003", "type": "Blueberry" },
                                { "id": "1004", "type": "Devil's Food" }
                            ]
                    },
                "topping":
                    [
                        { "id": "5001", "type": "None" },
                        { "id": "5002", "type": "Glazed" },
                        { "id": "5005", "type": "Sugar" },
                        { "id": "5007", "type": "Powdered Sugar" },
                        { "id": "5006", "type": "Chocolate with Sprinkles" },
                        { "id": "5003", "type": "Chocolate" },
                        { "id": "5004", "type": "Maple" }
                    ]
        }
        results = search_json_recursively(json_data, key)
        if len(results) == 0:
            assert True
        else:
            LOGGER.error(f"[ FAILURE ]: {label} found unexpected key ({key}) in json ({json_data})")
            assert False, f"found unexpected key ({key}) in json ({json_data})"
