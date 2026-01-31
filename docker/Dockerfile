FROM python:3.12-slim

# All repos will be mounted here at runtime
WORKDIR /workspace

# Install minimal tools needed for reproduction
RUN pip install --no-cache-dir pytest

# Default reproduction command
# (Can be overridden at runtime if needed)
CMD ["pytest"]
