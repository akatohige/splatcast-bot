FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -U pip \
 && pip install --no-cache-dir -r requirements.txt

COPY ./src/*.py ./
COPY ./webhook_url.txt ./

ENTRYPOINT ["python", "app.py"]