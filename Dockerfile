FROM tiangolo/uvicorn-gunicorn:python3.8-slim

COPY requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove gcc python-dev

RUN pip install --no-cache-dir -r /app/requirements.txt 

EXPOSE 8080

COPY . /app

# CMD uvicorn api:app --host 0.0.0.0 --port 8080
# CMD ["python", "main.py"]
