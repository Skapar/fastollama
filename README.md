# FastOllama

FastOllama - это REST API, разработанное на Python с использованием FastAPI. Оно использует Ollama и TinyLlama для обработки текстовых запросов, а также MongoDB, PostgreSQL и Redis в качестве хранилищ данных. Доступ к API осуществляется через Basic Authentication.

## Установка

### Требования

- Docker
- Docker Compose

### Шаги установки

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/fastollama.git
    cd fastollama
    ```

2. Создайте файл [.env](http://_vscodecontentref_/1) в корне проекта и добавьте следующие переменные окружения:

    ```plaintext
    # PostgreSQL
    POSTGRES_USER=postgres_username
    POSTGRES_PASSWORD=postgres_password
    POSTGRES_DB=db_name
    DATABASE_URL=postgresql://postgres_username:postgres_password@postgres:5432/db_name

    # MongoDB
    MONGO_URL=mongodb://mongodb:27017/db_name_mongo

    # Redis
    REDIS_URL=redis://redis:6379/0
    ```

3. Запустите Docker Compose для развертывания всех необходимых сервисов:

    ```bash
    docker-compose up --build -d
    ```

## Использование

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/register" -H "Content-Type: application/json" -d '{"username": "test_user", "password": "secure_password"}'
curl -X POST "http://localhost:8000/api/process" -H "Content-Type: application/json" -u test_user:secure_password -d '{"text": "Как дела?"}'
curl -X GET "http://localhost:8000/api/history" -u test_user:secure_password
```

```bash
http://localhost:8000/docs
```