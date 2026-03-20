# --- 第一阶段：直接使用官方运行镜像，不用 builder 了 ---
FROM caddy:2 AS caddy_official

# --- 第二阶段：构建你的 PHP 环境 ---
FROM php:8.2-fpm-alpine

# 安装 PHP 扩展（如 pdo_mysql 等）
RUN docker-php-ext-install pdo_mysql bcmath

# 【关键点】从官方镜像直接把二进制文件拷贝过来
COPY --from=caddy_official /usr/bin/caddy /usr/bin/caddy

# 设置工作目录
WORKDIR /srv

# 拷贝项目文件和配置
COPY . .
COPY Caddyfile /etc/caddy/Caddyfile

# 暴露端口
EXPOSE 80

# 启动 PHP-FPM 和 Caddy
# 使用 caddy run 时指定配置文件路径
CMD ["sh", "-c", "php-fpm -D && caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"]
