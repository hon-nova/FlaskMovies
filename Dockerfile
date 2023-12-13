FROM python:3.9
WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY static ./static
COPY templates ./templates

RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5000
CMD ["python", "app.py"]
