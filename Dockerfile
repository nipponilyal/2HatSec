From python:2.7

COPY intr/* /etc/
COPY requirements.txt /etc

WORKDIR /etc
RUN pip install -r /etc/requirements.txt

CMD ["python", "/etc/json-handler.py"]
