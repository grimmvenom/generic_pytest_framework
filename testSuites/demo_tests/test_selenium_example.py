#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath('./'))
sys.path.append(os.path.abspath('../../'))
import pytest
import time
from framework.modules.httpRequests import *
from framework.modules.selenium_methods import *


TestCase = os.path.basename(__file__)


class Test_Selenium_Demo:

    @classmethod
    def setup_class(self) :  # Setup Method to run before all class tests
        self.driver = pytest_determine_browser()

    @classmethod
    def teardown_class(self):  # Teardown Method to run after all class tests are complete
        try:
            self.driver.close()
        except:
            pass

    def setup_method(self, method):  # Setup method to run at start of each test method
        pytest.variables['method_name'] = f"{method.__name__}"
        pytest.variables['errors'] = list()

    def teardown_method(self, method):
        pass


    def test_basic_steps(self):
        self.driver.get("http://www.python.org")
        assert "Python" in self.driver.title
        elem = self.driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in self.driver.page_source
        time.sleep(5)
        self.driver.close()

