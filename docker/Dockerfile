# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Copy the LMS app into the container
COPY . /home/frappe/frappe-bench/

# Expose Frappe default port
EXPOSE 8000

# Optional: define env variables from Render dashboard
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

# Default start command for Frappe
CMD ["bench", "start"]
