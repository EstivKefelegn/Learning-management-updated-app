# Dockerfile
FROM frappe/erpnext:v15.85.0

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Copy your LMS app code into the container
COPY . /home/frappe/frappe-bench/

# Expose the Frappe default port
EXPOSE 8000

# Default start command
CMD ["bench", "start"]
