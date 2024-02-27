# Nirvana Senior Backend Engineer (Data) Interview Exercise

This repository contains the take-home exercise for the Nirvana Senior Backend Engineer (Data) interview.
See [here](https://docs.google.com/document/d/1l6VWk-qknOKiCeSV0M-C7gYcD20aJNEuctWy7ADj2y0) for the full prompt

## Overview

The docker-compose.yaml includes the following services:

- **coverage-api**: FastAPI service that serves as the primary backend application.
- **mock-clearinghouse-api**: FastAPI service acting as a mock clearinghouse API.
- **mysql_db**: MySQL database with a table named "overrides" and seed data (see overrides-seed-data)
- **mongo_db**: Empty MongoDB instance that the coverage API writes to. Default db is "nirvana"

## Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

## How to Run

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/nirvana-backend-exercise.git
   ```

2. Navigate to the project directory:

   ```bash
   cd data-take-home
   ```

3. Run the following Docker Compose command to start the services:

   ```bash
   docker-compose up -d
   ```

   This command will build the Docker images and start the containers in detached mode.

4. Wait for the services to start. You can check the logs using:

   ```bash
   docker-compose logs -f
   ```

   Once you see messages indicating that the services are ready, you can proceed.

5. The services should now be accessible:

   - **coverage-api**: http://localhost:8000
   - **mock-clearinghouse-api**: http://localhost:8001
   - **MySQL Database**: Host: `localhost`, Port: `3306`, Database: `nirvana`, User: `root`, Password: `root`
   - **MongoDB**: Host: `localhost`, Port: `27017`

## Usage

### Coverage API

You can interact with the services using the provided FastAPI endpoints. 

- **coverage-api Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

You have to provide a header `customer-id` for writing to mongodb.  

Here is a sample curl request from customer 1, for a request that does not have a manual override: 
```bash
curl --request POST \
  --url http://localhost:8000/ \
  --header 'Authorization: da382b16-83d3-4cc5-83e0-db862536cfbe' \
  --header 'Content-Type: application/json' \
  --header 'customer-id: 1' \
  --data '{
	"payer_id": "60054",
	"member_id": "ZZ1234567",
	"member_dob": "2001-01-01"
}'
```

Here is a sample curl request that has a manual override:
```bash
curl --request POST \
  --url http://localhost:8000/ \
  --header 'Authorization: da382b16-83d3-4cc5-83e0-db862536cfbe' \
  --header 'Content-Type: application/json' \
  --header 'customer-id: 2' \
  --data '{
	"payer_id": "60054",
	"member_id": "A27941657",
	"member_dob": "1991-03-23"
}'
```

## Cleanup

To stop and remove the Docker containers, run:

```bash
docker-compose down
```

## Notes

- Please do not touch the mock-clearinghouse-api, as this is mocking an external service. 
- The MySQL database includes a table named "overrides" with sample seed data.
- The MongoDB instance is initially empty and is used by the coverage API.

Feel free to explore the code and modify the configuration files as needed.
