FROM python:3.10
WORKDIR /code

RUN apt-get update && apt-get upgrade --yes

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
EXPOSE 3025

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3025"]
