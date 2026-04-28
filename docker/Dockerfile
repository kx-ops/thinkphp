FROM debian:11.11-slim

ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg2 lsb-release \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && curl -sS https://packages.sury.org/php/apt.gpg | gpg --dearmor > /usr/share/keyrings/php.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/php.gpg] https://packages.sury.org/php/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/php.list \
    && curl https://unit.nginx.org/keys/nginx-keyring.gpg > /usr/share/keyrings/nginx.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/nginx.gpg] https://packages.nginx.org/unit/debian/ $(lsb_release -cs) unit" > /etc/apt/sources.list.d/unit.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    procps unit unit-php libphp7.4-embed php7.4-cli php7.4-common php7.4-pdo php7.4-redis \
    php7.4-gd php7.4-mysql php7.4-mbstring php7.4-xml php7.4-curl php7.4-zip php7.4-bcmath runit \
    && rm -rf /var/lib/apt/lists/* && apt-get clean && apt-get autoremove -y

WORKDIR /thinkphp
COPY . .
COPY /docker/unit.json /var/lib/unit/conf.json
COPY /docker/services /etc/service
RUN chown -R unit:unit /thinkphp /var/lib/unit && \
    chmod -R 755 /thinkphp /var/lib/unit && rm -rf docker

RUN chmod -R +x /etc/service
CMD ["runsvdir", "-P", "/etc/service"]
