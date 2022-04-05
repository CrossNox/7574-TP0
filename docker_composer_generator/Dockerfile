FROM python:3.9.7-slim
COPY utils.py /
COPY generator.py /
COPY docker-compose-template.j2 /
COPY requirements.txt /

WORKDIR /

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "generator.py"]
