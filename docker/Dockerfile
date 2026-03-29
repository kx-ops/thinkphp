FROM php:8.3-fpm-alpine

RUN apk add --no-cache \
    nginx \
    libpq-dev \
    $PHPIZE_DEPS \
    linux-headers \
    # ------------------------------------
    && docker-php-ext-install pdo pdo_mysql \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apk del $PHPIZE_DEPS \
    && rm -rf /tmp/pear \
    # ------------------------------------
    && mkdir -p /run/nginx

COPY ./docker/nginx.conf /etc/nginx/http.d/default.conf
COPY ./docker/www.conf /usr/local/etc/php-fpm.d/www.conf

COPY ./src /var/www/html

RUN chown -R www-data:www-data /var/www/html

RUN printf "#!/bin/sh\nphp-fpm -D\nexec nginx -g 'daemon off;'\n" > /entrypoint.sh && chmod +x /entrypoint.sh
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]