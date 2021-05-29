#!/bin/bash
docker build --no-cache -t crypto-trader .
winpty docker run -it --rm --name python-crypto-trader  crypto-trader