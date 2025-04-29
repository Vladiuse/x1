# Проект Link Hub

Этот проект использует Django с Django REST Framework и Postgres в качестве базы данных. Весь проект контейнеризирован с использованием Docker и Docker Compose для простоты развёртывания.

## Запуск проекта с использованием Docker

### 1. Установка зависимостей

Убедитесь, что у вас установлен [Docker](https://www.docker.com/get-started) и [Docker Compose](https://docs.docker.com/compose/install/) на вашей машине.

### 2. Клонирование репозитория

Клонируйте репозиторий с кодом проекта:

```
git clone https://github.com/yourusername/link-hub.git
```
### 3. Создание .env файла
есть 2 файлы .env-example (в корне проекта и а папке app) - добавте переменные согластно описанию

POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD — эти параметры нужны для конфигурации PostgreSQL (используются внутри docker-compose.yml).

DB_USERNAME, DB_DBNAME, DB_PASSWORD, DB_HOST, DB_PORT — конфигурация подключения Django к базе данных.

DJANGO_SECRET_KEY — секретный ключ Django. Обязательно сгенерируйте новый перед продакшн-запуском.

TEMPLATE_ID, PUBLIC_KEY, SERVICE_ID — параметры для почтового сервиса (например, EmailJS или другого).


### 4. Запуск Docker контейнеров

После того как файл .env будет готов, можно запустить приложение с помощью Docker Compose. Выполните следующую команду:

```commandline
docker-compose up --build
```

###  Доступ к приложению
Django приложение: http://localhost:8000

Swagger документация API: http://localhost:8000/swagger/

Админка Django: http://localhost:8000/admin/