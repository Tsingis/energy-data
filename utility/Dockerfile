FROM mcr.microsoft.com/playwright:v1.56.1-noble

WORKDIR /app

COPY client/.npmrc ./
COPY client/package*.json ./
COPY client/src ./src
COPY client/tsconfig.json ./
COPY client/vite.config.ts ./
COPY client/playwright.config.ts ./

RUN npm ci && npm run build