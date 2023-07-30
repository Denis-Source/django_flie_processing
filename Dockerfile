FROM python:3.10

# Install Pandoc and Texlive
RUN apt-get update && apt-get install -y pandoc texlive \
    && rm -rf /var/lib/apt/lists/*

# Copy workdir
WORKDIR /django_file_processing
COPY . /django_file_processing/

# Copy and install dependancies
COPY requirements.txt /django_file_processing/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
