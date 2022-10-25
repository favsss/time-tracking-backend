# FROM public.ecr.aws/lambda/python:3.7
# # directory setup

# COPY ./requirements.txt ./requirements.txt

# RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# COPY ./app ./app

# # command to launch the api as well as use the certificates for https
# # CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["app.main.handler"]


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

