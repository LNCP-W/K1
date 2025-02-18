# K1 Project

A project for collecting and displaying information about the latest currency blocks.

This project uses **Celery** to periodically collect data via API requests, which is then saved to a database. For displaying data, a combination of **Django** and **FastAPI** is used.

## Setup and Running

### Steps to Set Up:

1. **Configure the `.env` file:**
   In this file, specify the following environment variables:
   - Database credentials
   - Django credentials
   - JWT secret for generating tokens
   - API domain

2. **Initialize SSL Certificates:**
   Run the script to initialize SSL certificates using Let's Encrypt:

   ```bash
   ./init-letsencrypt.sh
   This step will generate SSL certificates for your domain.

3. Start Docker Containers: Once the certificates are in place, start the Docker containers:

   ```bash
    docker-compose up -d
   
4. Once the containers are up and running, your project will be available at your domain.

### API Documentation:
You can access the API documentation here:

[https://\<domain>/docs/](https://\<domain>/docs/)

### Admin Panel Access:
The admin panel is accessible via the following URLs:

- [https://\<domain>/admin/](https://\<domain>/admin/)
- [https://\<domain>/django/admin](https://\<domain>/django/admin)

Use the credentials that you have defined in the Django `.env` file to log in.

## Technologies Used:

- **Celery**: Used for asynchronous task processing to collect and save data.
- **Django**: Responsible for interacting with the database and providing the admin panel.
- **FastAPI**: Used to build the API that serves the currency block data.
- **Docker**: Containers the entire project for easy deployment.
- **Let's Encrypt**: Used to obtain SSL certificates for secure communication.

