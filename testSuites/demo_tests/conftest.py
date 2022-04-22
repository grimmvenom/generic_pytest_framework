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


