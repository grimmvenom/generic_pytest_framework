#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
from pathlib import Path
import platform

# Global Variables
home = str(Path.home())  # User Home Directory
operating_system = str(platform.system())
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
parent_parent = os.path.abspath(os.path.join(parent_dir, os.pardir))
date = time.strftime("%m-%d-%Y") # Date Format mm-dd-yyyy_Hour_Min
Time = time.strftime("%H_%M") # Time
report_time = time.strftime("%I_%M_%p")
sys_time = time.strftime("%I_%M_%p")
log_date = time.strftime("%Y-%m-%d %I_%M_%s")

# Log Directory Variables
root_dir = os.path.realpath('./')
log_dir = f"{root_dir}{os.sep}logs"
framework_log_dir = f"{log_dir}{os.sep}results"
framework_log_name = f"results-{str(date)}_{str(report_time)}.log"
framework_log = f"{framework_log_dir}result.log"

allure_dir = f"{log_dir}{os.sep}allure_results"
allure_report_dir = f"{log_dir}{os.sep}report"
allure_report_tests = f"{allure_report_dir}{os.sep}Tests"

http_success_codes = [200, 201, 202, 301, 302]
http_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
supported_browsers = ['Chrome', 'Headless', 'Firefox', 'IE', 'Edge', 'Safari']
common_network_interfaces = {
    'Darwin': ['en0'],
    'Linux': ['eth0', 'wlan0'],
    'Windows': ['Ethernet']}

directories = [log_dir, framework_log_dir, allure_dir, allure_report_dir]

print(f"CONFIG Current Dir: {current_dir}")
print(f"LOGGER Path: {framework_log}")
# Setup / Configuration of local directories
for directory in directories:
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:
        print(f"Issue creating directory: {e}")
        pass

try:
    if os.path.exists(framework_log):
        os.remove(framework_log)
except Exception as e:
    print(f"Issue removing {framework_log}")
    pass
    
# LOGGER = logging.getLogger(__name__)
FORMAT = '%(levelname)s:%(asctime)s:%(filename)s:%(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, filename=framework_log)
LOGGER = logging.getLogger()
