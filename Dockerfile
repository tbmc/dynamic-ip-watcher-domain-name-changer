FROM python:3.8-alpine
MAINTAINER tbmc
WORKDIR /app
COPY . /app
RUN pip install -r requirements/common.txt

CMD ["python", "ip_listener.py"]
