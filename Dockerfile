FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir websocket
RUN pip install --no-cache-dir websocket-client
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "bot"]