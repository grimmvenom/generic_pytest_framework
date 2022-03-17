#!/bin/bash

cd ..

docker run \
    -p 0.0.0.0:8675:8675 \
    -it --entrypoint zsh \
    -v $(pwd):/pytest_framework \
    pytest-framework:latest