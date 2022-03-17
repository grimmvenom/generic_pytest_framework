#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summary:
    Trigger / execute unit tests for Framework Modules

"""

import os
import time
import shutil
import argparse

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
root_dir = os.path.realpath('../../../')
date = time.strftime("%m-%d-%Y")  # Date Format mm-dd-yyyy_Hour_Min
Time = time.strftime("%H_%M")
report_time = time.strftime("%I_%M_%p")
sys_time = time.strftime("%I_%M_%p")

log_dir = f"{root_dir}{os.sep}logs"
unit_test_log_dir = f"{log_dir}{os.sep}unit_test_results"
log_path = f"{unit_test_log_dir}{os.sep}unitTest.log"
new_log_path = f"{unit_test_log_dir}{os.sep}{date}_{report_time}-unitTest.log"
html_output = f"{unit_test_log_dir}{os.sep}{date}-{Time}-unitTestSuite.html"
allure_dir = f"{log_dir}{os.sep}allure_results"

print(f"Current Dir: {current_dir}")
print(f"root dir: {root_dir}")
print(f"Log Path: {new_log_path}")


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", action='store', dest='environment', default='dev', choices=['dev', 'qa', 'debug'], help='-e <environment>')
    parser.add_argument("--config", action='store', dest='config_path', help='--config <config_path>')
    parser.add_argument("-o", "--output", action='store', dest='output_type', default='both', choices=['html', 'allure', 'both'], help='-o <output>')
    parser.add_argument("-t", "--test", action='store', dest='test', help='-h <testCase>')
    parser.add_argument("-k", "--pattern", action='append', dest='patterns', help='-k methodname or pattern')
    arguments = parser.parse_args()
    command = f"py.test"
    if arguments.environment:
        os.environ['environment'] = str(arguments.environment)

    if arguments.config_path:
        os.environ['config_path'] = str(arguments.config_path)

    if arguments.output_type == "both":  # Run html and allure reporting
        command += f" --html={html_output} --self-contained-html --alluredir={allure_dir} --clean-alluredir"
    elif arguments.output_type == "html":  # Run html reporting
        command += f" --html={html_output} --self-contained-html"
    elif arguments.output_type == "allure":  # Run allure reporting
        command += f" --alluredir={allure_dir} --clean-alluredir"
    
    command += f" -vs ./"
    if arguments.test:
        if not arguments.test.endswith('.py'):
            arguments.test += ".py"
        command += f"{os.sep}{arguments.test} -sv"
    if arguments.patterns:
        for pattern in arguments.patterns:
            command += f" -k {pattern}"
    return arguments, command


def setup():
    if not os.path.exists(os.path.abspath(log_dir)):
        os.makedirs(log_path)
    if not os.path.exists(os.path.abspath(unit_test_log_dir)):
        os.makedirs(unit_test_log_dir)


def teardown():
    try:
        shutil.rmtree(f"./testSuites/unitTests/.pytest_cache")  # Cleanup pytest cache
    except Exception as e:
        pass

    pycache_paths = ['__pyache__/', './testSuites/__pycache__/', './testSuites/unitTests/__pycache__/']
    for path in pycache_paths:
        try:
            shutil.rmtree(path)  # Cleanup pycache
        except Exception as e:
            pass


setup()
arguments, command = get_arguments()
print(f"Command:\n{command}")
os.system(command)  # Run returned command
os.rename(log_path, new_log_path)  # Rename log output w/ unique name
teardown()
