# Builder
FROM python:3.8-slim as builder

COPY ./requirements.txt ./

RUN apt update \
    && apt install -y --no-install-recommends libjpeg-dev zlib1g-dev libfreetype6-dev \
    && pip3 install --trusted-host pypi.python.org --user -r requirements.txt

# Executor
FROM python:3.8-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY ./do.py ./

CMD ["python3", "-u", "do.py"]