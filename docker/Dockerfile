# 使用官方 PHP 8.3 FPM Alpine 镜像
FROM php:8.3-fpm-alpine

# 安装系统依赖及 PHP 扩展 (包含 Redis，不含 opcache)
RUN apk add --no-cache \
    nginx \
    libpq-dev \
    # --- 编译 Redis 扩展所需的临时工具 ---
    $PHPIZE_DEPS \
    linux-headers \
    # ------------------------------------
    && docker-php-ext-install pdo pdo_mysql \
    # 使用 pecl 安装 redis
    && pecl install redis \
    && docker-php-ext-enable redis \
    # --- 清理编译工具，减小镜像体积 ---
    && apk del $PHPIZE_DEPS \
    && rm -rf /tmp/pear \
    # ------------------------------------
    && mkdir -p /run/nginx

# 配置 Nginx
COPY ./docker/nginx.conf /etc/nginx/http.d/default.conf
COPY ./docker/www.conf /usr/local/etc/php-fpm.d/www.conf

# 复制源码
COPY ./src /var/www/html

# 设置权限
RUN chown -R www-data:www-data /var/www/html

# 启动脚本：同时启动 PHP-FPM 和 Nginx
CMD php-fpm -D && nginx -g "daemon off;"