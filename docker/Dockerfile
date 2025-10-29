# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Create logs directory (no chown needed)
RUN mkdir -p /home/frappe/frappe-bench/logs

# Copy LMS app into container
COPY . /home/frappe/frappe-bench/

# Expose default Frappe port
EXPOSE 8000

# Use the frappe user from base image
USER frappe

# Start Frappe
CMD ["bench", "start"]