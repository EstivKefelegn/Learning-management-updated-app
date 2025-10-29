# Use official Frappe/ERPNext image
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Copy LMS app into container as frappe user
COPY --chown=frappe:frappe . /home/frappe/frappe-bench/apps/lms/

# Switch to frappe user
USER frappe

# Install the LMS app
RUN cd /home/frappe/frappe-bench && \
    pip install -e apps/lms

# Build assets
RUN cd /home/frappe/frappe-bench && \
    bench build --app lms

# Expose default Frappe port
EXPOSE 8000

# Use production command
CMD ["bench", "production"]