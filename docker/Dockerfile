FROM frappe/erpnext:v15.85.0

WORKDIR /home/frappe/frappe-bench

COPY . /home/frappe/frappe-bench/

EXPOSE 8000

# Environment variable for logs (Render will mount /workspace at runtime)
ENV FRAPPE_LOGS_DIR=/workspace/logs

CMD ["bench", "start"]
