ARG tag=latest
FROM python:3.14-slim-bullseye AS build-image-dev1
LABEL maintainer="oldspiceap@gmail.com"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project files to a temporary folder
COPY . /tmp/emerald_heart/
WORKDIR /tmp/emerald_heart/

# Install build dependencies
RUN apt-get update
RUN apt-get install -y build-essential libpython3-dev python3-dev libxml2-dev libxslt-dev libjpeg-dev

ENV PYTHONPATH=/emerald_heart/lib/python3.14/site-packages:/emerald_heart/lib64/python3.14/site-packages
ENV DJANGO_STATIC_ROOT=/emerald_heart/static/
ENV SECRET_KEY="tmp-build-key"
#                    -O: Strips asserts and docstrings for smaller install
#      /tmp/emerald_heart: The package source folder
# --prefix=/emerald_heart: The destination installation environment folder
RUN uv pip install --prefix=/emerald_heart .
RUN python /emerald_heart/lib/python3.14/site-packages/emerald_heart/manage.py collectstatic --noinput --clear -i input.css -i video.js

# Create static folder from which to serve static files
RUN mkdir -p /emerald_heart/static/

# Create folder for on-disk cache
RUN mkdir -p /emerald_heart/volume/query_cache/

FROM python:3.14-slim-bullseye

ENV PYTHONPATH=/emerald_heart/lib/python3.14/site-packages:/emerald_heart/lib64/python3.13/site-packages
ENV DJANGO_SETTINGS_MODULE=emerald_heart.settings.production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies
RUN apt-get update && apt-get install -y ffmpeg supervisor nginx && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

# Create required folders
RUN mkdir -p /var/log/supervisor/
RUN mkdir -p /var/log/gunicorn/
RUN mkdir -p /var/log/nginx/
RUN mkdir -p /etc/supervisor/conf.d/
RUN mkdir -p /etc/nginx/conf.d/
RUN mkdir -p /var/run/gunicorn/
RUN mkdir -p /emerald_heart/volume/query_cache/
RUN mkdir -p /emerald_heart/volume/db/
RUN mkdir -p /emerald_heart/volume/uploads/
RUN mkdir -p /emerald_heart/volume/upload_temp/

# Copy in configuration files
COPY --from=build-image-dev1 /tmp/emerald_heart/conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY --from=build-image-dev1 /tmp/emerald_heart/conf/gunicorn.conf.py /emerald_heart/gunicorn.conf.py
COPY --from=build-image-dev1 /tmp/emerald_heart/conf/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-image-dev1 /tmp/emerald_heart/conf/emerald.conf /etc/nginx/conf.d/emerald.conf
COPY --from=build-image-dev1 /tmp/emerald_heart/conf/migrate.sh /emerald_heart/bin/migrate.sh

# Grab the pre-built app from the build-image.
COPY --from=build-image-dev1 /emerald_heart /emerald_heart
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

EXPOSE 8080
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
