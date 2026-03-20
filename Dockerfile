# --- 第一阶段：获取 Caddy 二进制文件 ---
FROM caddy:2-builder AS caddy_builder

# --- 第二阶段：构建最终镜像 ---
FROM php:8.2-fpm-alpine

# 安装常用的 PHP 扩展（根据需求增减）
RUN docker-php-ext-install pdo_mysql bcmath

# 从第一阶段复制 Caddy
COPY --from=caddy_builder /usr/bin/caddy /usr/bin/caddy

# 设置工作目录
WORKDIR /srv

# 复制项目代码
COPY . .

# 复制 Caddy 配置文件
COPY Caddyfile /etc/caddy/Caddyfile

# 暴露 80 端口
EXPOSE 80

# 启动脚本：同时启动 PHP-FPM 和 Caddy
# 使用 sh -c 来同时运行两个进程
CMD ["sh", "-c", "php-fpm -D && caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"]
