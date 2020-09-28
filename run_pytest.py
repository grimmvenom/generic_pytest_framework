#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summary:
	To Trigger / execute pytest test suite

"""

import requests
import os
import time

# Global Variables
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
date = time.strftime("%m-%d-%Y")  # Date Format mm-dd-yyyy_Hour_Min
Time = time.strftime("%H_%M")  # Time
report_time = time.strftime("%I_%M_%p")
sys_time = time.strftime("%I_%M_%p")

log_path = f"{current_dir}{os.sep}logs{os.sep}pytest_results{os.sep}pytest.log"
new_log_path = f"{current_dir}{os.sep}logs{os.sep}pytest_results{os.sep}pytest-{date}_{report_time}.log"

html_output = f"{current_dir}{os.sep}logs{os.sep}pytest_results{os.sep}{date}-{Time}-pytest_suite.html"
html_args = f" --html={html_output} --self-contained-html"

allure_dir = f"{current_dir}{os.sep}logs{os.sep}allure_results"
allure_args = f" --alluredir={allure_dir} --clean-alluredir"

both_args = html_args + allure_args

# os.system("py.test" + str(html_args) + " -vs ./Generic/")  # Run html reporting
# os.system("py.test" + str(allure_args) + " -vs ./Generic/")  # Run Allure reporting
# os.system("py.test" + str(both_args) + " -vs ./Generic/")  # Run html and allure reporting

os.system("py.test" + str(both_args) + " -vs ./framework/tests/API/")  # Run html and allure reporting
# os.system("py.test" + str(allure_args) + " -vs ./framework/tests/API/")


# os.system("py.test" + str(both_args) + " -vs ./tests/Test/")  # Run html and allure reporting
os.rename(log_path, new_log_path)  # Rename log output w/ unique name



