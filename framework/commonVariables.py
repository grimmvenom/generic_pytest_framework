#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: grimmvenom <grimmvenom@gmail.com>
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

http_success_codes = [200, 201, 202, 301, 302]
http_methods = ["GET", "POST", "PUT", "DELETE"]
supported_browsers = ['Chrome', 'Headless', 'Firefox', 'IE', 'Edge', 'Safari']
common_network_interfaces = {'Darwin': ['en0'],
                             'Linux': ['eth0', 'wlan0'],
                             'Windows': ['Ethernet']}

LOGGER = logging.getLogger(__name__)
