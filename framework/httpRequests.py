#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: nick serra <nserra@riis.com>

Summary:
    Common API / HTTP request methods

"""

from framework.commonMethods import *
from http.client import responses
from lxml.html import fromstring
import requests
import urllib3
import ast
from fake_useragent import UserAgent


def generate_user_agent(browser):
    ua = eval("UserAgent()." + browser)
    return ua


class ApiRequest:
    def __init__(self, method: str, url: str, data: dict, json_payload: dict, headers: dict):
        self.method = method.lower()
        self.url = url
        self.data = data
        self.json_payload = json_payload
        self.headers = headers

    def perform_request(self):
        request_start_time = time.time()
        string = "self.url"
        if bool(self.data):
            string = string + ", data=self.data"
        if bool(self.json_payload):
            string = string + ", json=self.json_payload"
        if bool(self.headers):
            string = string + ", headers=self.headers"
        
        results = eval("requests." + str(self.method.lower()) + "(" + string + ")")
        LOGGER.info(f"Status Code: {results.status_code}, Content: {results.content}")
        if len(results.text) >= 1:
            try:
                content = results.json()
            except Exception as e:
                print(f"APIRequests content ({results.content}) to json ERROR: {e}")
                LOGGER.error(f"APIRequests content ({results.content}) to json ERROR: {e}")
                try:
                    content = json.loads(results.text)
                except Exception as e:
                    print(f"APIRequests content ({results.content}) to text ERROR: {e}")
                    content = str(results.text)
                    LOGGER.error(f"APIRequests content ({results.content}) to text ERROR: {e}")
        else:
            content = dict()
        status_code = str(results.status_code)
        response_headers = results.headers
        
        end_time = time.time() - request_start_time
        duration = format(end_time / 60, '.2f')

        result_data = {"URL": self.url,
                       "Method": self.method,
                       "Data": self.data,
                       "JSON": self.json_payload,
                       "Headers": self.headers,
                       "response_content": content,
                       "response_status_code": status_code,
                       "response_header": response_headers,
                       "execution_time": f"{duration} min"}
        
        if int(status_code) in http_success_codes:
            LOGGER.info(f"httpRequests.py:ApiRequests:perform_request: {self.method.upper()}: SUCCESS:: {self.url} -> Status Code: {status_code}")
            LOGGER.info(result_data)
        else:
            LOGGER.warn(f"httpRequests.py:ApiRequests:perform_request: {self.method.upper()}: WARNING:: {result_data}")
        return result_data


class RequestSession:
    def __init__(self, method: str, url: str, data: dict, json_payload: dict, headers: dict):
        self.session = requests.session()
        self.method = method.lower()
        self.url = url
        self.data = data
        self.json_payload = json_payload
        self.headers = headers
        self.redirect_limit = 5
    
    def session_response(self):
        request_start_time = time.time()
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response_data = dict()
        # print([element_url, element_type, element_index])
        response_data["url"] = str(self.url)

        string = "self.url"
        if bool(self.data):
            string = string + ", data=self.data"
        if bool(self.json_payload):
            string = string + ", json=self.json_payload"
        if bool(self.headers):
            string = string + ", headers=self.headers"
            
        try:
            response = eval("self.session." + str(self.method) + "(" + string + " (, stream=True, verify=False, allow_redirects=self.redirect_limit)")
            end_time = time.time() - request_start_time
            duration = format(end_time / 60, '.2f')
            
            response_data["execution_time"] = f"{duration} min"
            # response = self.session.get(self.url, data=self.data, headers=self.headers, stream=True, verify=False,
            #                             allow_redirects=self.redirect_limit)
            if response.history:
                hist = list()
                response_data["status_code"] = str(response.history[0].status_code)
                response_data["redirectedURL"] = response.url
                response_data["message"] = str(responses[int(response.history[0].status_code)])
                hist.append(self.url)
                for item in response.history:
                    hist.append(item.url)
                hist.append(response.url)
                response_data["redirect_trace"] = hist
                response_data["redirect_count"] = str(len(hist))
                # print("Redirect_History: " + str(url) + " --> " + str(hist))
            else:
                response_data['status_code'] = response.status_code
                response_data["message"] = str(responses[int(response.status_code)])
            tree = fromstring(response.content)
            response_data["pageTitle"] = tree.findtext('.//title')
    
        except requests.sessions.TooManyRedirects as e:
            response_data['status_code'] = "ERROR"
            response_data['message'] = "MAX REDIRECTS: " + str(e)
            response_data['pageTitle'] = "N/A"
            response_data["redirect_trace"] = list()
    
        except Exception as e:
            response_data['status_code'] = "ERROR"
            response_data['message'] = str(e)
            response_data['pageTitle'] = "N/A"
            response_data["redirect_trace"] = list()
            
        if len(response.content) > 0:
            return dict(response_data), str(response.content.decode("utf-8"))
        else:
            return dict(response_data)

    
class StageRequests:
    def __init__(self):
        self.staged_requests = dict()
        self.completed_requests = dict()
    
    def stage_request(self, context):
        for row in context.table:
            row_data = {"URL": row["URL"],
                        "Method": row["Method"],
                        "Data": ast.literal_eval(row["Data"]),
                        "JSON": ast.literal_eval(row["JSON"]),
                        "Headers": ast.literal_eval(row["Headers"])}
            if 'request' in context.config.userdata.keys():
                if 'Headers' in context.config.userdata['request'].keys():
                    if 'Headers' not in row_data.keys():
                        row_data['Headers'] = dict()
                    for key, value in context.config.userdata['request']['Headers'].items():
                        row_data['Headers'][str(key)] = value
                if 'Data' in context.config.userdata['request'].keys():
                    if 'Data' not in row_data.keys():
                        row_data['Data'] = dict()
                    for key, value in context.config.userdata['request']['Data'].items():
                        row_data['Data'][str(key)] = value
                
            LOGGER.info("httpRequests.py:StageRequests:stage_request: staging:: " + str(row_data))
            index = len(self.staged_requests.keys()) + 1
            self.staged_requests[str(index)] = row_data
    
    def http_request_json(self, requirements):
        url = requirements["URL"]
        method = requirements["Method"]
        data = requirements["Data"]
        json_payload = requirements["JSON"]
        headers = requirements["Headers"]
        LOGGER.info("httpRequests.py:StageRequests:http_request_json: requesting: " + str(requirements))
        # results = requests.get(url, data=data, headers=headers)
        request_start_time = time.time()
        
        results = eval("requests." + str(method.lower()) + "(url, data=data, headers=headers)")

        end_time = time.time() - request_start_time
        duration = format(end_time / 60, '.2f')
        
        try:
            content = results.json()
        except Exception as e:
            print(e)
            content = json.loads(results.text)
        status_code = str(results.status_code)
        response_headers = results.headers
        result_data = {"URL": url,
                       "Method": method,
                       "Data": data,
                       "JSON": json_payload,
                       "Headers": headers,
                       "response_content": content,
                       "response_status_code": status_code,
                       "response_header": response_headers,
                       "execution_time": f"{duration} min"}
        
        index = len(self.completed_requests.keys()) + 1
        self.completed_requests[str(index)] = result_data
    
        if int(status_code) in http_success_codes:
            LOGGER.info(f"httpRequests.py:StageRequests:http_request_json: {method.upper()}: SUCCESS:: {url}  -> Status Code: {status_code}")
        else:
            LOGGER.warn(f"httpRequests.py:StageRequests:http_request_json: {method.upper()}: WARNING:: {result_data}")
    


