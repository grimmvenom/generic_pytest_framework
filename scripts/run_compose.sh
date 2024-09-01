#!/bin/bash

cd ..

sudo docker compose -f docker-compose.yml up
## In another terminal window run:
# sudo docker container exec -it pytest-framework zsh