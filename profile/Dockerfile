FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Используем shell форму для поддержки аргументов
CMD python app.py $DEBUG_FLAG