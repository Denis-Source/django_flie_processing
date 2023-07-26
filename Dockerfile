FROM python:3.10

# Install Pandoc
RUN apt-get update && apt-get install -y pandoc \
    && rm -rf /var/lib/apt/lists/*

# Copy workdir
WORKDIR /django_file_processing
COPY . /django_file_processing/

# Copy and install dependancies
COPY requirements.txt /django_file_processing/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for outside connections
EXPOSE 8000
CMD ["python3", "main.py"]