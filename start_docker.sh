#!/bin/bash

# SOURCE THIS FILE 
# ----------------
# build command:
#   docker build -t soonmeet-rest-api:1.0-slim .

docker run --rm -it -p 8000:8000 soonmeet-rest-api:1.0-slim

# --rm        -> remove instance after stop
# -it         -> interactive (output to tty)
# -e DEBUG=1  -> to enable debugging
