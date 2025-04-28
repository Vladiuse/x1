FROM python:3.11
WORKDIR /app
COPY . /app/
RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install -r requirements.txt
CMD python3 manage.py migrate \
    && python manage.py collectstatic --no-input \
    && gunicorn link_hub.wsgi:application --bind 0.0.0.0:8000 --log-level info