# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Copy LMS app into container
COPY . /home/frappe/frappe-bench/

# Expose default Frappe port
EXPOSE 8000

# Use Render writable logs directory
ENV FRAPPE_LOGS_DIR=/workspace/logs

# Start Frappe
CMD ["bench", "start"]
