# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Create logs directory with proper permissions
RUN mkdir -p /home/frappe/frappe-bench/logs && \
    chown -R frappe:frappe /home/frappe/frappe-bench && \
    chmod -R 755 /home/frappe/frappe-bench/logs

# Copy LMS app into container
COPY . /home/frappe/frappe-bench/

# Fix permissions after copy
RUN chown -R frappe:frappe /home/frappe/frappe-bench && \
    chmod -R 755 /home/frappe/frappe-bench/logs

# Expose default Frappe port
EXPOSE 8000

# Start Frappe
CMD ["bench", "start"]