#!/bin/bash
source .venv/bin/activate
source .vscode/env.sh

cd src

python3 test/source_data_gen.py