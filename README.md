[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Tsingis_energy-data&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Tsingis_energy-data)

Project about energy consumption and production in Finland. Open source data from [Fingrid](https://data.fingrid.fi/en/datasets)

Tools used:

- Python 3.13
- Node.js 22
- Docker

**Instructions:**

Docker

- Run via Docker `docker compose up --build`

Server

- Create python virtual environment `python -m venv venv`
- Activate virtual environment `.\venv\Scripts\activate`
- Install dependencies `pip install -r server\requirements.txt`
- Launch `python server\src\main.py`

Client

- Navigate to client directory `cd client`
- Install dependencies `npm install`
- Launch `npm run dev`
