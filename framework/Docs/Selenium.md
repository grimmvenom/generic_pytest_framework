# Selenium

## Resources:
- [Selenium with Docker](https://github.com/SeleniumHQ/docker-selenium)
- [Selenium Docker Compose GitHub](https://github.com/SeleniumHQ/docker-selenium/tree/trunk?tab=readme-ov-file)


## Troubleshoot standalone selenium containers
- http://localhost:7900/?autoconnect=1&resize=scale&password=secret 



## Run Selenium Firefox service using Docker
There are plenty of other browser selenium images available

Run Docker Selenium-Firefox container using name selenium:
```
docker run -d -p 0.0.0.0:4444:4444 -p 0.0.0.0:7900:7900 -p 0.0.0.0:4317:4317 -v /dev/shm:/dev/shm --name firefox selenium/standalone-firefox:4.24.0-20240830
```

Run docker container interactively while linking to named firefox selenium container
```
docker run -p 0.0.0.0:8675:8675 --link firefox:firefox -it --entrypoint /usr/bin/fish pytest-framework:latest
```


Share folder with host (execute from pytest_framework parent directory:)
```
docker run -p 0.0.0.0:8675:8675 -it --entrypoint /usr/bin/fish --link firefox:firefox -v $(pwd):/pytest_framework pytest-framework:latest
```