FROM frappe/erpnext:v15.85.0

WORKDIR /home/frappe/frappe-bench

COPY . /home/frappe/frappe-bench/

EXPOSE 8000

# Logs directory that is writable on Render
ENV FRAPPE_LOGS_DIR=/workspace/logs

# Start Frappe
CMD ["bench", "start"]
