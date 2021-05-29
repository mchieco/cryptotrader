FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install websocket
RUN pip install websocket-client
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "bot"]