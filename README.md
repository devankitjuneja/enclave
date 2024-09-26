
# Enclave Secret Manager

## Overview

Enclave Secret Manager is a secure solution for managing sensitive information, such as API keys, credentials, and other secrets. It ensures that secrets are encrypted, versioned, and securely stored in a PostgreSQL database. It comes with a robust API and CLI that interact with the core library, making it easy to integrate secret management into your workflows.

## Features
- **Secret Encryption**: Supports encryption of secrets using AES and other algorithms.
- **Versioning**: Secrets can have multiple versions, with the ability to switch between versions.
- **API and CLI**: Access and manage secrets via a REST API or a command-line interface.
- **Dockerized Deployment**: Easily deploy and run using Docker and Docker Compose.

## Running Locally

### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- PostgreSQL (local or dockerized)
- Poetry for dependency management

### Setting Up the Virtual Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/devankitjuneja/enclave.git
   cd enclave
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

4. Set up your environment variables by creating a `.env` file:
   ```bash
   touch .env
   ```

   Populate the `.env` file with the following environment variables:
   ```env
   API_URL=http://localhost:8000
   API_KEY=<your-api-key>
   POSTGRES_DB=enclave
   POSTGRES_USER=enclave
   POSTGRES_PASSWORD=enclave
   POSTGRES_HOST=localhost
   REDIS_HOST=localhost
   ```

5. Run the application locally:
   ```bash
   poetry run uvicorn enclave.api.main:app --reload
   ```

6. Open your browser and navigate to `http://localhost:8000/docs` to explore the API.

### Running with Docker Compose (Recommended)

1. Ensure Docker and Docker Compose are installed on your machine.
2. Set up your environment variables by creating a `.env` file:
   ```bash
   touch .env
   ```

   Populate the `.env` file with the following environment variables:
   ```env
   API_URL=http://enclave-api:8000
   API_KEY=<your-api-key>
   POSTGRES_DB=enclave
   POSTGRES_USER=enclave
   POSTGRES_PASSWORD=enclave
   POSTGRES_HOST=enclave-db
   REDIS_HOST=enclave-redis
   ```
3. Navigate to the project directory where the `docker-compose.yml` file is located.
4. Run the following command to start the services:
   ```bash
   docker compose up --build
   ```
   This command will:
   - Build the API image
   - Set up the PostgreSQL database
   - Seed the database with initial data from the `db-scripts` folder

5. Once the services are up, you can access the API at `http://localhost:8000` and PostgreSQL on `localhost:5432`.

6. To stop the services, run:
   ```bash
   docker compose down
   ```

## Usage

### API Endpoints

You can interact with the Secret Manager through its API:

- **Create a Secret**:
   ```bash
   POST /secrets
   {
     "name": "db-password",
     "value": "s3cr3tp@ssw0rd"
   }
   ```

- **Retrieve a Secret**:
   ```bash
   GET /secrets/{secret_name}
   ```

- **Update a Secret**:
   ```bash
   PUT /secrets/{secret_name}
   {
     "value": "newS3cr3t"
   }
   ```

- **Delete a Secret**:
   ```bash
   DELETE /secrets/{secret_name}
   ```

### CLI Usage

You can also interact with the Secret Manager using its CLI:

- **Create a Secret**:
   ```bash
   enclave-cli create --name db-password --value s3cr3tp@ssw0rd
   ```

- **Retrieve a Secret**:
   ```bash
   enclave-cli read --name db-password --version 1
   ```

- **Update a Secret**:
   ```bash
   enclave-cli update --name db-password --value newS3cr3t
   ```

- **Delete a Secret**:
   ```bash
   enclave-cli delete --name db-password
   ```

## Contributing

We welcome contributions! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.
