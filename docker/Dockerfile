# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Fix permissions as root first
USER root

# Reinstall Frappe in development mode
RUN cd /home/frappe/frappe-bench && \
    pip install -e apps/frappe

# Create logs directory with proper permissions
RUN mkdir -p /home/frappe/frappe-bench/logs && \
    chown -R frappe:frappe /home/frappe/frappe-bench && \
    chmod -R 755 /home/frappe/frappe-bench/logs

# Copy LMS app into container
COPY --chown=frappe:frappe . /home/frappe/frappe-bench/apps/lms/

# Install LMS app in development mode
RUN cd /home/frappe/frappe-bench && \
    pip install -e apps/lms

# Ensure permissions are correct
RUN chown -R frappe:frappe /home/frappe/frappe-bench/logs && \
    chmod 755 /home/frappe/frappe-bench/logs

# Expose default Frappe port
EXPOSE 8000

# Switch to frappe user
USER frappe

# Start Frappe
CMD ["bench", "start"]