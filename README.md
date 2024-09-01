# Generic Pytest Framework

## Requirements:
<hr>

- python3+
- python3+ pip
- [allure](https://docs.qameta.io/allure/)
- Selenium (optional)

<br>

## Getting Started
- [Framework Setup Instructions](./framework/Docs/Framework_Setup.md)
- add any necessary environments & variables you wish to use to config.ini

<br>

## Other helpful Documentation
- [Docker Cheatsheet](./framework/Docs/Docker.md)
- [Docker Resources](./framework/Docs/Docker.md)
- [Selenium](https://selenium-python.readthedocs.io/)
- [Selenium Resources](./framework/Docs/Selenium.md)

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

## To Run Demo Tests Locally - Requires Local Selenium Setup
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

## Build pytest-framework image With Docker
<hr>

Build pytest-framework image using docker:
```
docker build --rm -t pytest-framework ./
```


<br>

## Run Demo tests with Docker Compose
- script examples: 
    - [build_docker.sh](./scripts/build_docker.sh)
    - [run_compose.sh](./scripts/run_compose.sh)

Build pytest-framework image using docker:
```
docker build --rm -t pytest-framework ./
```


Run docker-compose.yml (firefox standalone selenium container):
```
cd ..
# Build container network of multiple containers
docker compose -f docker-compose.yml up

# connect to pytest_framework terminal after container is started
docker container exec -it pytest_framework zsh
```

To run the demo tests via container:
```
cd /pytest_framework
python ./run_functional_tests.py -e demo -p demo
```
<br>