FROM python:3.9-slim

WORKDIR /app

COPY load_cats_script.py .

RUN pip install minio requests

CMD ["python", "load_cats_script.py"]