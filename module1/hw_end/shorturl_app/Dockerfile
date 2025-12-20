FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

VOLUME /app/data

EXPOSE 80
# пока крон робит раз в 30 секунд. В проде можно сделать раз в сутки ночью
HEALTHCHECK --interval=30s --timeout=2s --start-period=5s --retries=3 \
  CMD python cleanup.py || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]