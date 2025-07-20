# Data Fetcher and Database Updater Application

## Overview

This application periodically fetches data from an external API and updates it in the database. On the first run, if no data exists in the database, the app automatically creates all necessary tables with proper relationships and populates them with data retrieved from the API.

Additionally, the app exposes an HTTP endpoint that returns a plain-text summary of the data currently stored in the database.

---

## Features

- Automatic database schema creation on first run if tables do not exist
- Periodic scheduled data fetching and updating from the external API
- HTTP endpoint to retrieve a text summary of the stored data
- Configurable fetch interval through environment variables

---

## Setup and Installation

1. **Clone the repository:**

    ```bash
    git clone git@github.com:Tepex651/sync_db.git
    cd sync_db
    ```

2. **Create a `.env` file** with the necessary environment variables:

    ```env
    POSTGRES_USER=youruser
    POSTGRES_PASSWORD=yourpassword
    POSTGRES_DB=yourdatabase
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    API_URL=https://api.example.com/data
    DATA_REFRESH_INTERVAL_SECONDS=3600
    ```

3. **Start the application and database with Docker Compose:**

    ```bash
    docker-compose up --build
    ```

This command will build the Docker image for the app, start the PostgreSQL database container, and launch the app container.

---

## Usage

- The application will automatically create database tables on the first run and populate them with data fetched from the external API.  
- The data fetching happens periodically based on the interval configured via `DATA_REFRESH_INTERVAL_SECONDS`.  
- Access the HTTP summary endpoint by opening a browser and navigating to:

    ```
    http://localhost:5555/info
    ```

This will display a plain-text report with aggregated data information such as product counts, categories, and marks

---

### Connecting to an External PostgreSQL Database

To connect the application to an existing external PostgreSQL database instead of the one provided by Docker Compose:

1. **Update your `.env` file** (or environment variables) with the external database credentials:

  ```env
  POSTGRES_HOST=<external-db-host>
  POSTGRES_PORT=<external-db-port>
  POSTGRES_USER=<your-username>
  POSTGRES_PASSWORD=<your-password>
  POSTGRES_DB=<your-database>
  ```

3. **Start only the `app` service** using Docker Compose without starting the `db` service:

  ```bash
  docker-compose up app
  ```

Alternatively, comment out or remove the `db` service section in `docker-compose.yml` if not needed.

---

## Configuration

All configuration options are managed via environment variables, including:

| Variable                   | Description                                  | Default                          |
|----------------------------|----------------------------------------------|---------------------------------|
| `POSTGRES_USER`            | PostgreSQL username                          | *required*                      |
| `POSTGRES_PASSWORD`        | PostgreSQL password                          | *required*                      |
| `POSTGRES_DB`              | PostgreSQL database name                     | *required*                      |
| `POSTGRES_HOST`            | Hostname or IP address of PostgreSQL server | `db` (service name in Compose)  |
| `POSTGRES_PORT`            | PostgreSQL port                              | *required*                          |
| `DATA_REFRESH_INTERVAL_SECONDS` | Interval in seconds between data fetches | `3600` (1 hour)                 |

---
