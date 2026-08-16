FROM python:3.9-slim

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m pip install --no-cache-dir --upgrade \
    "setuptools>=78.1.1" \
    "wheel>=0.47.0" \
    "jaraco.context>=6.1.1"

COPY app.py .
EXPOSE 8080
CMD ["python3", "app.py"]
