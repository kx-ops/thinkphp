FROM php:8.3.30-alpine3.22

RUN apk add --no-cache \
        unit-php83 \
        unit \
    && apk add --no-cache --virtual .build-deps \
        $PHPIZE_DEPS \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apk del .build-deps && rm -rf /tmp/pear

WORKDIR /thinkphp
COPY . .
COPY /conf.json /var/lib/unit/conf.json
RUN mkdir -p /var/log/unit && chown -R unit:unit /var/log/unit

CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock", "--log", "/dev/stdout"]
