# Запуск сервисов локально

### Для To Do
```
cd todo_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Для Shortener

```
cd url_shortener
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

# Запуск сервисов через Docker

```
docker build -t todo-service ./todo_service
docker build -t url-shortener ./url_shortener

docker volume create todo_data
docker volume create shorturl_data

docker run -d -p 8000:80 -v todo_data:/app/data --name todo_container todo-service
docker run -d -p 8001:80 -v shorturl_data:/app/data --name url_container url-shortener
```
