# Framework Setup Instructions

- Install Python 3+
- Install Pip 3 (Python Package Manager)
- In terminal / cmd prompt (to install required packages)
    ```
    python -m pip install -r requirements.txt
    ```
- Download Supported Selenium Webdrivers from under the "Selenium Web Driver Setup" section
- Add these executable files under a directory named “selenium” somewhere on your system
- Add your “selenium” directory to your PATH / environmental variables so the executables can be called as a command
- To test, simply type driver name --version
    ````
    Example: chromedriver --version or chromedriver.exe --version
    ````
- if on MacOS, you may need to allow your browser to run automation. To do this go to System Preferences -> Security & Privacy -> General

<br>

## Selenium Web Driver Setup
To leverage Selenium locally, it is important to download the right browser drivers that support the version of the web browser you are using. Safari and Edge are supported by default
- Chrome - [Chromedriver](https://sites.google.com/chromium.org/driver/downloads)
- Mozilla Firefox - [Geckodriver](https://github.com/mozilla/geckodriver/releases/)
- MS Edge - [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- Safari - Covered by default on MacOS