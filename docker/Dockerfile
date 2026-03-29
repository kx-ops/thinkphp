# ====================== Stage 1: 构建依赖（变化少，缓存友好） ======================
FROM php:8.3-fpm-alpine AS builder

# 安装构建依赖 + 运行时必要包
RUN apk add --no-cache \
    nginx \
    libpq-dev \
    $PHPIZE_DEPS \
    linux-headers \
    && docker-php-ext-install pdo pdo_mysql \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apk del $PHPIZE_DEPS \
    && rm -rf /tmp/pear /var/cache/apk/*

# 如果你的项目使用 Composer（ThinkPHP 大多使用），强烈建议加上以下部分
# WORKDIR /app
# COPY ./src/composer.json ./src/composer.lock ./
# RUN composer install --no-dev --optimize-autoloader --no-scripts --prefer-dist

# ====================== Stage 2: 最终运行镜像（轻量） ======================
FROM php:8.3-fpm-alpine

# 复制已安装的 PHP 扩展（复用 builder 阶段）
COPY --from=builder /usr/local/lib/php/extensions /usr/local/lib/php/extensions
COPY --from=builder /usr/local/etc/php/conf.d /usr/local/etc/php/conf.d

# 安装运行时必要包（nginx + 少量依赖）
RUN apk add --no-cache nginx \
    && mkdir -p /run/nginx /var/www/html/runtime \
    && chown -R www-data:www-data /var/www/html

# 复制配置文件（变化不频繁）
COPY ./docker/php-optimized.ini /usr/local/etc/php/conf.d/custom.ini
COPY ./docker/nginx.conf /etc/nginx/http.d/default.conf
COPY ./docker/www.conf /usr/local/etc/php-fpm.d/www.conf

WORKDIR /var/www/html

# 最后复制应用代码（变化最频繁，放最后 → 缓存利用率最高）
COPY ./src /var/www/html

# 设置权限
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# 创建 entrypoint
RUN printf '#!/bin/sh\nphp-fpm -D\nexec nginx -g "daemon off;"\n' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

USER www-data

EXPOSE 80
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]