#!/bin/bash
docker build -t crypto-trader .
winpty docker run -it --rm --name python-crypto-trader  crypto-trader