FROM frappe/erpnext:v15.85.0

WORKDIR /home/frappe/frappe-bench

COPY . /home/frappe/frappe-bench/

EXPOSE 8000

# Environment variables (Render will inject these)
ENV DB_HOST=${DB_HOST} \
    DB_PORT=${DB_PORT} \
    DB_NAME=${DB_NAME} \
    DB_USER=${DB_USER} \
    DB_PASSWORD=${DB_PASSWORD} \
    REDIS_CACHE=${REDIS_CACHE} \
    REDIS_QUEUE=${REDIS_QUEUE} \
    REDIS_SOCKETIO=${REDIS_SOCKETIO} \
    ALLOW_SIGNUP=${ALLOW_SIGNUP} \
    DEVELOPER_MODE=${DEVELOPER_MODE} \
    FRAPPE_LOGS_DIR=/workspace/logs

CMD ["bench", "start"]
