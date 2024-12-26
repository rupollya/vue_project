# фронт
FROM node:18 AS frontend

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

RUN npm run build


# бэкенд
FROM python AS final

RUN apt-get update && \
    apt-get install -y mariadb-server nginx

WORKDIR /app

COPY --from=frontend /app/frontend/dist /usr/share/nginx/html

COPY backend/ ./backend
WORKDIR /app/backend
RUN pip install -r requirements.txt

RUN service mariadb start && \
    mariadb -e "CREATE DATABASE IF NOT EXISTS task_manager;" && \
    mariadb -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '505750'; FLUSH PRIVILEGES;"

COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80
EXPOSE 8003

ENV PYTHONPATH=/app

CMD service mariadb start && \
    sleep 5 && \
    service nginx start && \
    gunicorn backend.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8003