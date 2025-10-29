# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Create and use writable directories for Render
RUN mkdir -p /tmp/logs /tmp/sites && \
    chmod 777 /tmp/logs /tmp/sites

# Create symlinks to writable directories
RUN ln -sf /tmp/logs /home/frappe/frappe-bench/logs && \
    ln -sf /tmp/sites /home/frappe/frappe-bench/sites

# Copy LMS app into container
COPY . /home/frappe/frappe-bench/

# Set environment variables for writable directories
ENV BENCH_LOG_FILE=/tmp/logs/bench.log
ENV FRAPPE_LOGS_DIR=/tmp/logs

# Expose default Frappe port
EXPOSE 8000

# Use the frappe user from base image
USER frappe

# Start Frappe
CMD ["bench", "start", "--port", "8000"]