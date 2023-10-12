FROM python:3.10

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu bionic main"
RUN apt update

# Install Pandoc, Texlive and tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr pandoc texlive  \
    && rm -rf /var/lib/apt/lists/*


# Copy workdir
WORKDIR /django_file_processing
COPY . /django_file_processing/

# Copy and install dependancies
COPY requirements.txt /django_file_processing/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
