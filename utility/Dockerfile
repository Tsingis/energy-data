FROM mcr.microsoft.com/playwright:v1.54.2-noble

WORKDIR /app

COPY client/package*.json ./
COPY client/.npmrc ./
COPY client/src ./src
COPY client/tsconfig.json ./
COPY client/vite.config.ts ./
COPY client/playwright.config.ts ./

RUN npm ci && npm run build

COPY client/tests/playwright ./tests/playwright

CMD ["npm", "run", "playwright"]