FROM python:3.8-alpine
MAINTAINER tbmc
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app

CMD ["python", "ip_listener.py"]
