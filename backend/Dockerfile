FROM python:3.9-slim

WORKDIR /app

COPY ./uva-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./uva-api .

EXPOSE 8000

CMD ["uvicorn", "uva-api:app", "--host", "0.0.0.0", "--port", "8000"]
