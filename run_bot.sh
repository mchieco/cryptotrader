#!/bin/bash
docker build -t crypto-trader .
docker run -it --rm --name python-crypto-trader  crypto-trader