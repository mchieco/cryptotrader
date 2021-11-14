FROM python:3.9-slim-buster

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y git

COPY requirements.txt ./

RUN pip install --no-cache-dir websocket
RUN pip install --no-cache-dir websocket-client
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "bot", "no-user"]