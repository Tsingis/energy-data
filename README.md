[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Tsingis_energy-data&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Tsingis_energy-data) [![Docker Scan](https://github.com/tsingis/energy-data/actions/workflows/scan.yml/badge.svg)](https://github.com/tsingis/energy-data/actions/workflows/scan.yml)

Project about energy consumption and production in Finland. Open source data from [Fingrid](https://data.fingrid.fi/en/datasets)

Energy price in Finland. API data from [Pörssisähkö](https://porssisahko.net/api)

Frontend: https://energy-data-client-r6oz7us4ea-lz.a.run.app

Backend: https://energy-data-server-r6oz7us4ea-lz.a.run.app/docs

Tools used:

- Python
- Node.js
- Vue
- Docker
- Google Cloud
- Terraform

**Instructions:**

Docker

- Run via Docker `docker compose up --build client server`

Server

- Navigate to server directory `cd server`
- Install uv globally `pip install -r requirements.txt`
- Set up environment `uv sync`
- Launch `uv run task api`

Client

- Navigate to client directory `cd client`
- Install dependencies `npm install`
- Launch `npm run dev`
