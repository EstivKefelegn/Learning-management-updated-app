# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Fix permissions as root first
USER root

# Create logs directory with proper permissions
RUN mkdir -p /home/frappe/frappe-bench/logs && \
    chown -R frappe:frappe /home/frappe/frappe-bench && \
    chmod -R 755 /home/frappe/frappe-bench/logs

# Copy LMS app into container
COPY --chown=frappe:frappe . /home/frappe/frappe-bench/

# Ensure permissions are correct
RUN chown -R frappe:frappe /home/frappe/frappe-bench/logs && \
    chmod 755 /home/frappe/frappe-bench/logs

# Expose default Frappe port
EXPOSE 8000

# Switch to frappe user
USER frappe

# Set port via environment variable (bench will auto-detect)
ENV PORT=8000

# Start Frappe
CMD ["bench", "start"]