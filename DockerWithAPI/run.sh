#!/bin/bash



pip install -r requirements.txt

cd src
# python /src/main.py --host  "0.0.0.0"  --port  "4000"  --reload
uvicorn main:app --host 0.0.0.0 --port 4000 --reload
