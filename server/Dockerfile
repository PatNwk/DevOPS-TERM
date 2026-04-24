FROM python:3-alpine3.23
WORKDIR /app
COPY server /app/server
COPY main.py /app/main.py
RUN pip install --no-cache-dir mysql-connector-python fastapi uvicorn
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
