# Stage 1: Build laye
FROM python:3.8.5-slim-buster AS builder
RUN apt update -y && apt install awscli -y

WORKDIR /app
COPY . /app

# Install dependencies into a virtual environment or temp dir
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Stage 2: Final lightweight image
FROM python:3.8.5-slim-buster

WORKDIR /app

# Copy only the installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy source code (you can filter if needed)
COPY --from=builder /app /app

CMD ["python3", "main.py"]
