#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resources:
    https://docs.pytest.org/en/latest
    https://docs.qameta.io/allure/
    https://github.com/allure-framework/allure2
    https://github.com/pytest-dev/pytest-html
    
# Test URLs:
    https://reqres.in/
    https://jsonplaceholder.typicode.com/guide.html

# Example Commands:
py.test test_generic_GET.py -vs  # Will run tests and print stdout
    py.test --alluredir=../allure_results
    py.test --alluredir=../allure_results --clean-alluredir -vs test_generic_GET.py  # Will run specific test and print stdout
    py.test test_generic_GET.py -k <method> -s  # Will run specific test + method and print stdout
    py.test -rA <file>   # Will execute test and give a quick summary at the end of stdout
    py.test --html=report.html --self-contained-html ./  # Generate HTML Output
    
    py.test --html=../Logs_PyTest/report.html --self-contained-html --alluredir=../allure_results --clean-alluredir -vs ./
"""

import os
import sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../'))
import pytest
import logging
import allure_pytest

from framework.commonVariables import *
from framework.httpRequests import *
from framework.commonMethods import *

# Global Variables
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

directories = ["logs", f"logs{os.sep}pytest_results", f"logs{os.sep}allure_results"]
# Setup / Configuration of local directories
for directory in directories:
    if not os.path.exists(f"{current_dir}{os.sep}{directory}"):
        os.makedirs(f"{current_dir}{os.sep}{directory}")
