# Generic Pytest Framework

## Requirements:
<hr>

- python3+
- python3+ pip
- [allure](https://docs.qameta.io/allure/)

<br>

## To Run Demo Tests
<hr>

Run all tests under testSuites/demo_tests
```
python ./run_functional_tests.py -e <env> -p demo
```

Run Specific test under testSuites/demo_tests
```
python ./run_functional_tests.py -e <env> -p demo -t <filename>
```

Run Specific Step within a test
```
python ./run_functional_tests.py -e <env> -p demo -t <filename> -k <functinoName or className>
```

<br>

## Docker
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
