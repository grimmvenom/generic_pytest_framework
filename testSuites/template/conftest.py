#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
import sys
import json
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../../'))
import configparser
from framework.modules.commonMethods import *

pytest.variables = dict()

def detect_auto_skip(variables):  # If auto_fail == True, skip test. Can be combined with setup_method to skip the rest of the test
    if variables["auto_fail"] == True:
        pytest.skip(f"{variables['fail_reason']}", allow_module_level=True)

pytest.variables['auto_fail'] = False
pytest.variables['fail_reason'] = str()


if "environment" in os.environ:
    env = os.environ["environment"]
else:
    env = "dev"
pytest.variables['env'] = env

if "config_path" in os.environ:
    config_path = os.environ["config_path"]
else:
    config_path = os.path.abspath('config.ini')
pytest.variables['config_path'] = config_path

config = configparser.ConfigParser()
config.read(config_path)
for key, value in config[env].items():
    if value.startswith('{') and value.endswith('}'):
        try:
            pytest.variables[str(key)] = json.loads(value)
        except:
            pass
    else:
        try:
            pytest.variables[str(key)] = str(value)
        except:
            pass
