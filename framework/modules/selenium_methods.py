import os
import sys
import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from framework.modules.commonVariables import *
import pytest
# from framework.modules.commonMethods import *

chrome_path_windows = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
chrome_path_linux = "/usr/bin/google-chrome"
chrome_path_mac = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"  


def determine_chrome_path():
    if platform.system() == "Darwin":  # if MacOS
        return chrome_path_mac
    elif platform.system() == "Win32":  # Windows
        return chrome_path_windows
    elif platform.system() == "Linux" or platform.system() == "Linux2": # linux
        return chrome_path_linux
    else:
        print("OS unknown, please open chrome manually with remote-debugging option")
        LOGGER.warning("OS unknown, please open chrome manually with remote-debugging option")
        return None


def open_chrome_browser_remote_debugger(url):
    LOGGER.info(f"Operating System: {platform.system()}")
    chrome_path = determine_chrome_path()
    command = f"{chrome_path} --remote-debugging-port=1559 {url}"
    LOGGER.info(f"Starting Chrome Debugger: {command}")
    os.popen(command)
    

def setup_chrome_browser():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(desired_capabilities=DesiredCapabilities.CHROME, chrome_options=options)
    LOGGER.info("Starting Selenium, Connecting to Chrome Debugger Address")
    return driver


def setup_chrome_browser_remote_debugger():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:1559");
    driver = webdriver.Chrome(desired_capabilities=DesiredCapabilities.CHROME, chrome_options=options)
    LOGGER.info("Connecting to Chrome Debugger Address")
    return driver


def setup_chrome_headless():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:1559");
    driver = webdriver.Chrome(desired_capabilities=DesiredCapabilities.CHROME, chrome_options=options)
    LOGGER.info("Starting Selenium using headless Chrome")
    return driver


def setup_firefox_browser():
    driver = webdriver.Firefox(desired_capabilities=DesiredCapabilities.FIREFOX)
    LOGGER.info(f"Starting Selenium using Firefox")
    return driver


def browser_wait_manual_intervention(self, message):
    start_time = time.time()
    LOGGER.info(f"Manual browser intervention required for: {message}")
    input(f"\n{message}\n")
    end_time = time.time() - start_time
    LOGGER.info(f"Manual Intervention took: {end_time} seconds")