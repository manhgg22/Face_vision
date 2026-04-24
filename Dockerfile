# base image
FROM python:3.10-slim

# -----------------------------------
# create required folder
RUN mkdir -p /app
WORKDIR /app

# -----------------------------------
# Install system dependencies for OpenCV and other libraries
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libhdf5-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------
# Copy required files from repo into image
COPY ./deepface /app/deepface
# even though we will use local requirements, this one is required to perform install deepface from source code
COPY ./requirements/requirements.txt /app/requirements.txt
COPY ./requirements/requirements_local.txt /app/requirements_local.txt
COPY ./package_info.json /app/
COPY ./setup.py /app/
COPY ./docs/README.md /app/README.md
COPY ./entrypoint.sh /app/deepface/api/src/entrypoint.sh

# -----------------------------------
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install the project in editable mode
RUN pip install -e . --no-deps

# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1

# -----------------------------------
# run the app (face_service.py runs on port 8001)
EXPOSE 8001
ENTRYPOINT [ "sh", "entrypoint.sh" ]
