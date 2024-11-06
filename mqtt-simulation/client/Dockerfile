FROM python:3.10-slim

WORKDIR /app

RUN pip install paho-mqtt

COPY test_light.py .

CMD [ "python", "test_light.py" ]

