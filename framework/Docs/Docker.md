# Docker CheatSheet

## Containers
Show running containers:  ``docker ps -a`` <br>
List exited containers: ``docker ps -a -f status=exited`` <br>
Cleanup old images that are exited:  ``docker rm $(docker ps -a -f status=exited -q)``<br>
Cleanup old docker containers: ``docker container prune`` <br>
List running ports: ``docker container ls --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" -a`` <br>
Stop all containers: ``docker stop $(docker ps -a -q)`` <br>
Remove all containers: ``docker rm $(docker ps -a -q)`` <br>


## Images
Show available images: ``docker images`` <br>
remove docker image:  ``docker rmi <image_id>`` <br>
cleanup images w/o at least one associated container: ``docker image prune -a`` <br>
Cleanup docker images: ``docker image prune`` <br>
build docker image from Dockerfile:  ``docker build --rm -t pytest_framework ./`` <br>

## Volumes
List Docker volumes: ``docker volume ls`` <br>
List Dangling Docker Volumes: ``docker volume ls -f dangling=true`` <br>
Remove Docker Volume: ``docker volume rm volume_name volume_name`` <br>
Remove Dangling Volumes: ``docker volume rm $(docker volume ls -f dangling=true -q)`` <br>

### Common Commands you will use
Build Application / Project as a docker Image:
```
docker build --rm -t pytest-framework ./
```

### Run docker containers individually (without docker compose):

Run Selenium Standalone Service:
```
    docker run -d -p 0.0.0.0:4444:4444 -p 0.0.0.0:5900:5900 -v /dev/shm:/dev/shm --name selenium selenium/standalone-chrome-debug:latest
```

Run pytest-framework interactively:
```
Run docker container interactively while linking to a named selenium container:
    docker run -p 0.0.0.0:8675:8675 --link selenium:selenium -it --entrypoint /usr/bin/fish pytest-framework:latest

Share folder with host (execute from pytestTests parent directory):
    docker run -p 0.0.0.0:8675:8675 -it --entrypoint /usr/bin/fish --link selenium:selenium -v $(pwd):/pytestTests pytest-framework:latest
```

### Run docker containers as a service (with docker compose):
```
Run Docker Compose services detached (in background)
    docker-compose up -d

Run pytest-framework container in interactive mode:
    docker-compose exec pytest-framework zsh
```