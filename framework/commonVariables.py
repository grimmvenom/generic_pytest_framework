#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: nick serra <nserra@riis.com>
=====================================================
# Common Variables for Testing
=====================================================
"""
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
p3 = os.path.abspath(os.path.join(parent_parent, os.pardir))
p4 = os.path.abspath(os.path.join(p3, os.pardir))
date = time.strftime("%m-%d-%Y") # Date Format mm-dd-yyyy_Hour_Min
Time = time.strftime("%H_%M") # Time
report_time = time.strftime("%I_%M_%p")
sys_time = time.strftime("%I_%M_%p")
log_date = time.strftime("%Y-%m-%d %I_%M_%s")

# Log Directory Variables
log_dir = f"{parent_parent}{os.sep}logs"
behave_log_dir = f"{log_dir}{os.sep}behave_results"
# behave_logging = log_dir + os.sep + "behave_results" + os.sep + "behave-" + str(date) + "_" + str(report_time) + ".log"

behave_log_dir = f"{log_dir}{os.sep}behave_results{os.sep}"
behave_log_name = f"behave-{str(date)}_{str(report_time)}.log"
behave_logging = f"{behave_log_dir}behave.log"

allure_dir = f"{log_dir}{os.sep}allure_results"
allure_report_dir = f"{log_dir}{os.sep}report"
allure_report_tests = f"{allure_report_dir}{os.sep}Tests"

http_success_codes = [200, 201, 202, 301, 302]
http_methods = ["GET", "POST", "PUT", "DELETE"]
supported_browsers = ['Chrome', 'Headless', 'Firefox', 'IE', 'Edge', 'Safari']
common_network_interfaces = {'Darwin': ['en0'],
                             'Linux': ['eth0', 'wlan0'],
                             'Windows': ['Ethernet']}

directories = [log_dir, behave_log_dir, allure_dir, allure_report_dir]

print(f"CONFIG Current Dir: {current_dir}")
print(f"LOGGER Path: {behave_logging}")
# Setup / Configuration of local directories
for directory in directories:
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:
        print(f"Issue creating directory: {e}")
        pass

try:
    if os.path.exists(behave_logging):
        os.remove(behave_logging)
except Exception as e:
    print(f"Issue removing {behave_logging}")
    pass
    
# LOGGER = logging.getLogger(__name__)
FORMAT = '%(levelname)s:%(asctime)s:%(filename)s:%(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, filename=behave_logging)
LOGGER = logging.getLogger()
