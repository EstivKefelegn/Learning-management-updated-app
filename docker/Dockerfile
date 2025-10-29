# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

WORKDIR /home/frappe/frappe-bench

COPY . /home/frappe/frappe-bench/

# Ensure logs directory exists and is writable
RUN mkdir -p /home/frappe/frappe-bench/logs \
    && chown -R frappe:frappe /home/frappe/frappe-bench/logs \
    && chmod -R 775 /home/frappe/frappe-bench/logs

EXPOSE 8000

ENV DB_HOST=${DB_HOST} \
    DB_PORT=${DB_PORT} \
    DB_NAME=${DB_NAME} \
    DB_USER=${DB_USER} \
    DB_PASSWORD=${DB_PASSWORD} \
    REDIS_CACHE=${REDIS_CACHE} \
    REDIS_QUEUE=${REDIS_QUEUE} \
    REDIS_SOCKETIO=${REDIS_SOCKETIO} \
    ALLOW_SIGNUP=${ALLOW_SIGNUP} \
    DEVELOPER_MODE=${DEVELOPER_MODE}

CMD ["bench", "start"]
