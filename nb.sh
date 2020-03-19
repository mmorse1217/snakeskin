#!/bin/bash
docker run --rm -p 8888:8888 -v `pwd`:/src snakeskin:latest \
    jupyter notebook --allow-root --port=8888 --ip=0.0.0.0 $@

