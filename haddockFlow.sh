#!/bin/bash

# Show the commands, and exit on errors
set -ex

# Move to correct directory
pushd ~/haddockFlow

# run python script
python haddockFlow.py

# go back where we came from
popd

