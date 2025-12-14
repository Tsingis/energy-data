FROM node:24.12.0-alpine3.23 AS build

WORKDIR /app

ENV NO_UPDATE_NOTIFIER=true

COPY package*.json ./
COPY .npmrc ./

RUN npm ci

ARG API_URL

ENV VITE_API_URL=${API_URL}

COPY src/ ./src
COPY tsconfig.json ./tsconfig.json
COPY vite.config.ts ./vite.config.ts

RUN sed -i "s|__API_URL__|${API_URL}|g" src/public/insert-links.js && \
    npm run build

FROM nginxinc/nginx-unprivileged:1.29.3-alpine3.22-slim

COPY --from=build /app/dist /usr/share/nginx/html
COPY /nginx/nginx.conf /etc/nginx/nginx.conf

ARG PORT=3000

RUN sed -i "s|__PORT__|${PORT}|g" /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]