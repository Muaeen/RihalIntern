#!/bin/bash

cd neural-api

pip install -r requirements.txt

python /src/main.py --host  "0.0.0.0"  --port  "4000"  --reload