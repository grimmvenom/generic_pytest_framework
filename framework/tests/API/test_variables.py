#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os, json
from conftest import *

TestCase = os.path.basename(__file__)


class test_variables:
	
	def test_variables(self):
		LOGGER.info(f"my variable: {pytest.my_environment}")