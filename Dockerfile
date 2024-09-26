# Use the official Python image from the Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install Poetry
RUN pip install poetry

# Install the dependencies defined in pyproject.toml
RUN poetry config virtualenvs.create false && poetry install


# Command to run the API
CMD ["poetry", "run", "uvicorn", "enclave.api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8005"]
