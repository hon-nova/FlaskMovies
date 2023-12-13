FROM python:3.9
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5000
CMD ["python", "app.py"]

