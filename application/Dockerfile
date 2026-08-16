FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade "wheel>=0.46.2,<0.48"
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
EXPOSE 8080
CMD ["python3", "app.py"]
