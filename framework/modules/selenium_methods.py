import os
import sys
import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from soupsieve import select
from framework.modules.commonVariables import *
import pytest
# from framework.modules.commonMethods import *

supported_browsers = ['firefox', 'chrome', 'headless', 'safari', 'edge']

chrome_path_windows = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
chrome_path_linux = "/usr/bin/google-chrome"
chrome_path_mac = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"  

remote = bool(pytest.variables['remote'])
headless = bool(pytest.variables['headless'])


def pytest_determine_browser():
    if "browser" in pytest.variables.keys():
        print(f"Browser Specified: {pytest.variables['browser']}")
        selected_browser = pytest.variables['browser'].lower()

        if selected_browser not in supported_browsers:
            LOGGER.error(f"selected browser ({selected_browser}) not supported, please use: ({supported_browsers})")
        
        elif selected_browser == 'firefox':
            LOGGER.info(f"Firefox browser specified")
            options = FirefoxOptions()
            # options.add_argument("--headless")
        
        elif selected_browser == 'chrome':
            LOGGER.info(f"Chrome browser specified")
            options = ChromeOptions()
            driver = webdriver.Chrome(desired_capabilities=DesiredCapabilities.CHROME, chrome_options=ChromeOptions())
        
        elif selected_browser == 'edge':
            LOGGER.info(f"Edge browser specified")
            driver = webdriver.Safari(options=selenium.webdriver.edge.options)
        
        elif selected_browser == 'safari':
            LOGGER.info(f"Safari browser specified")
            driver = webdriver.Safari(options=selenium.webdriver.safari.options)

        else:
            options = None
            LOGGER.error(f"selected browser not supported. Please ensure it is in {supported_browsers}")
            exit(1)

        if remote and headless:
            LOGGER.info(f"remote {selected_browser} browser specified w/ headless option")
            options.add_argument('headless')
            # options.add_experimental_option("debuggerAddress", "127.0.0.1:1559");
            driver = webdriver.Remote(options=options, command_executor=f"{pytest.variables['remote_url']}")
        elif remote and not headless:
            LOGGER.info(f"remote {selected_browser} browser specified")
            driver = webdriver.Remote(options=options, command_executor=f"{pytest.variables['remote_url']}")
        else:
            driver = webdriver.Remote(options=options)
            
        return driver
    else:
        LOGGER.error("browser not specified in config.ini")
        return None


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
    


def browser_wait_manual_intervention(self, message):
    start_time = time.time()
    LOGGER.info(f"Manual browser intervention required for: {message}")
    input(f"\n{message}\n")
    end_time = time.time() - start_time
    LOGGER.info(f"Manual Intervention took: {end_time} seconds")