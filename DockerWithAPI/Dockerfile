FROM python:3.11

WORKDIR /neural-api

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src /neural-api


# CMD ["python", "main.py","--host", "0.0.0.0", "--port", "4000", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]