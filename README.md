[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Tsingis_energy-data&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Tsingis_energy-data) [![Deploy Server](https://github.com/tsingis/energy-data/actions/workflows/server_deploy.yml/badge.svg)](https://github.com/tsingis/energy-data/actions/workflows/server_deploy.yml) [![Deploy Client](https://github.com/tsingis/energy-data/actions/workflows/client_deploy.yml/badge.svg)](https://github.com/tsingis/energy-data/actions/workflows/client_deploy.yml)

Project about energy consumption and production in Finland. Open source data from [Fingrid](https://data.fingrid.fi/en/datasets)

Energy price in Finland. API ata from [Pörssisähkö](https://porssisahko.net/api)

Frontend: https://energy-data-client.onrender.com

Backend: https://energy-data-server.onrender.com/docs

Tools used:

- Python 3.13
- Node.js 22
- Docker

**Instructions:**

Docker

- Run via Docker `docker compose up --build`

Server

- Navigate to server directory `cd server`
- Create python virtual environment `python -m venv venv`
- Activate virtual environment `.\venv\Scripts\activate`
- Install dependencies `pip install -r requirements.txt`
- Launch `python src\main.py`

Client

- Navigate to client directory `cd client`
- Install dependencies `npm install`
- Launch `npm run dev`
