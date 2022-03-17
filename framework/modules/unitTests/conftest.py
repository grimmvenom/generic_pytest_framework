#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
import sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../../'))
import configparser

def detect_auto_skip(variables):
    if variables["auto_fail"] == True:
        pytest.skip(f"{variables['fail_reason']}", allow_module_level=True)

"""
    Environment Setup
"""
pytest.variables = dict()

if "environment" in os.environ:
    env = os.environ["environment"]
else:
    env = "dev"

if "config_path" in os.environ:
    config_path = os.environ["config_path"]
else:
    config_path = os.path.abspath('../../config.ini')

config = configparser.ConfigParser()
config.read(config_path)
for key, value in config[env].items():
    try:
        pytest.variables[str(key)] = str(value)
    except:
        pass
pytest.variables['auto_fail'] = False
pytest.variables['fail_reason'] = str()
