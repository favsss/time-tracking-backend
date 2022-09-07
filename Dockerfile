FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./localhost+1-key.pem /code/localhost+1-key.pem

COPY ./localhost+1.pem /code/localhost+1.pem

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--ssl-keyfile=./localhost+1-key.pem", "--ssl-certfile=./localhost+1.pem"]

