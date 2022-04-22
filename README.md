# Generic Pytest Framework

## Requirements:
<hr>

- python3+
- python3+ pip
- [allure](https://docs.qameta.io/allure/)

<br>

## Getting Started
- [Framework Setup](./framework/Docs/Framework_Setup.md)
- copy example_config.ini to config.ini
- add any necessary environments & variables you wish to use to config.ini

<br>

## Other Documentation
- [Selenium](https://selenium-python.readthedocs.io/)
- [Docker Cheatsheet](./framework/Docs/Framework_Setup.md)


<br>

## How To Add New Projects
- copy testSuites/template -> testSuites/{whatever}_tests
- if adding a new project, update project_choices variable in run_functional_tests.py

## How to Add New Tests:
- copy rename test_example.py -> test_{scenario}.py

## Things to keep in mind:
- config.ini defines environments and variables for that environment
- conftest.py within the testSuite defines what happens before any of the tests are executed
- test suites need to be named test_{whatever}.py
- test steps also must contain test_{whatever}
- helper methods can be defined and do not need test_ naming convention in method name
- you can import some common methods defined under pytest_framework/framework/modules
- If something doesn't exist yet, we can build it or import more packages from pip

<br>

## To Run Demo Tests Locally
<hr>

Required Parameters:
- ``-e <env>`` 
- ``-p <project>``

View Framework Launcher Supported Parameters:
```
python ./run_functional_tests.py -h
```

Run all tests under testSuites/demo_tests
```
python ./run_functional_tests.py -e demo -p demo
```

Run Specific test under testSuites/demo_tests
```
python ./run_functional_tests.py -e demo -p demo -t <filename>
```

Run Specific Step within a test
```
python ./run_functional_tests.py -e demo -p demo -t <filename> -k <functinoName or className>
```

<br>

## Run With Docker
<hr>

Build Docker:
```
docker build --rm -t pytest-framework ./
```


Run Docker Selenium-Chrome container using name selenium:
```
docker run -d -p 0.0.0.0:4444:4444 -p 0.0.0.0:5900:5900 -v /dev/shm:/dev/shm --name selenium selenium/standalone-chrome-debug:latest
```


Run docker container interactively while linking to named selenium container
```
docker run -p 0.0.0.0:8675:8675 --link selenium:selenium -it --entrypoint /usr/bin/fish pytest-framework:latest
```


Share folder with host (execute from pytest_framework parent directory:)
```
docker run -p 0.0.0.0:8675:8675 -it --entrypoint /usr/bin/fish --link selenium:selenium -v $(pwd):/pytest_framework pytest-framework:latest
```

<br>
