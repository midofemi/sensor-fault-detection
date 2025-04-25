# === Stage 1: Build dependencies ===
FROM python:3.8.5-slim-buster AS builder

WORKDIR /build

# Install build tools
RUN apt-get update && apt-get install -y \
    build-essential gcc g++ libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the full project early so setup.py is available for editable install
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Optional: install the local project if not already handled in requirements.txt
RUN pip install --user .


# === Stage 2: Final image ===
FROM python:3.8.5-slim-buster

WORKDIR /app

# Install runtime tools (like awscli if needed)
RUN apt-get update && apt-get install -y awscli && rm -rf /var/lib/apt/lists/*

# Copy dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy your application code (only needed parts; we use . here for simplicity)
COPY . .

# Setup environment so Python finds the installed packages
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/root/.local:$PYTHONPATH"

# Optional: expose the port your app runs on
EXPOSE 8080

# Start the app
CMD ["python", "main.py"]

