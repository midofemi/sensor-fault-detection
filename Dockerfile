# === Builder Stage ===
FROM python:3.8.5-slim-buster as builder

# Set working directory
WORKDIR /build

# Install system-level build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency files first for caching
COPY requirements.txt .

# Install Python dependencies into a user-specific location
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install the project (if using setup.py, otherwise skip this line)
RUN pip install --user .



# === Final Stage ===
FROM python:3.8.5-slim-buster

# Set working directory
WORKDIR /app

# Optional: Install awscli (only if needed at runtime)
RUN apt-get update && apt-get install -y awscli && rm -rf /var/lib/apt/lists/*

# Copy installed packages from the builder
COPY --from=builder /root/.local /root/.local

# Copy project source
COPY . .

# Ensure Python can find the installed packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/root/.local:$PYTHONPATH



# Run your app
CMD ["python", "main.py"]
