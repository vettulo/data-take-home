# Nirvana Senior Backend Engineer (Data) Interview Exercise -> Proposal

This is the proposal for this project.

## Architecture

### Initial Diagram

Summary: 

1. Coverage API service requests ClearingHouse API for member data
2. Some of the data is overriden with overrides table
3. Consolidated data is stored in MongoDB
4. Response is returned

![Initial Architecture Diagram](/static/initial.jpg?raw=true "Initial Architecture Diagram")

### Proposed Architecture

![Proposed Architecture Diagram](/static/proposal.jpg?raw=true "Proposed Architecture Diagram")

1. Coverage API service requests ClearingHouse API for member data
2. Some of the data is overriden with overrides table
3. Consolidated data is stored in MongoDB
4. Consolidated data + additional data is stored in Coverage RAW **NEW!**
5. Respose is returned

Also we have two pipelines (Dagster) **NEW!**
- Overrides Pipeline: gets the same data from overrides table (once a day for example) -> Not implemented for now
- Coverage Pipeline: process coverage_raw and adds data to api_calls and members (hourly for example)

And data visualization (Metabase) **NEW!**
- Gets data from coverage_raw, api_calls, members and overrides_raw
- Allows users to create dashboards

## Overview

The docker-compose.yaml includes the following services:

- **coverage-api**: FastAPI service that serves as the primary backend application.
- **mock-clearinghouse-api**: FastAPI service acting as a mock clearinghouse API.
- **mysql_db**: MySQL database with a table named "overrides" and seed data (see overrides-seed-data)
- **mongo_db**: Empty MongoDB instance that the coverage API writes to. Default db is "nirvana"

**NEW!**
- **dagster-daemon**: Dagster Daemon to run pipelines.
- **dagster-webserver**: Dagster UI to see the pipelines and make configurations
- **mysql_db_analytics**: MySQL database to handle analytics
- **metabase**: Metabase for data visualization



## How to run

1. Run the following Docker Compose command to start the services:

   ```bash
   docker-compose build
   docker-compose up -d
   ```


2. The services should now be accessible:

   - **coverage-api**: http://localhost:8000
   - **mock-clearinghouse-api**: http://localhost:8001
   - **MySQL Database**: Host: `localhost`, Port: `3306`, Database: `nirvana`, User: `admin`, Password: `password`
   - **MongoDB**: Host: `localhost`, Port: `27017`

   **NEW!**
   - **MySQL Analytics**: Host: `localhost`, Port: `3307`, Database: `analytics`, User: `admin_analytics`, Password: `password_analytics`
   - **Dagster**: Host: `localhost`, Port: `3000`
   - **Metabase**: Host: `localhost`, Port: `3002` User: `admin@admin.com`, Password: `admin12345`

Note: to connect to MySQL directly or from metabase you need to configure `allowpublickeyretrieval=true`

## Notes

- Environment variables should be added to all services and this repository, as well as secrets in docker/docker compose
- Code quality could be improved, recommended to use precommit with pylint, black and mypy. Also add docstrings and comments.
- Unit tests are necessary for the api and dagster pipelines
- Pipelines should be able to be scheduled and allow the transactions to be idempotent
- Write to analytics should be async

## Future improvements

- Use a datawharehouse instead of MySQL if necessary (more expensive but faster for analytics)
- Add DBT for transformations (easy to combine with dagster)