FROM python:3.13-alpine AS build

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && \
    python -m pip uninstall -y setuptools wheel pip

FROM python:3.13-alpine

WORKDIR /app

COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY ./src .

RUN rm -r /usr/local/lib/python3.13/site-packages/pip*

RUN addgroup -S app && adduser -S -G app api
USER api

CMD ["python", "main.py"]