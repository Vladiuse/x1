# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt

#CMD ["gunicorn", "link_hub.wsgi:application", "--bind", "0.0.0.0:8000"]

CMD python manage.py migrate \
    && python manage.py collectstatic --no-input \
    && gunicorn link_hub.wsgi:application --bind 0.0.0.0:8000