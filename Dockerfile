# 使用基于 nginx:1.25.3 的官方 nginx 镜像
#FROM nginx:1.25.0-bullseye
FROM nginx:1.25.3
# 将当前目录的 pi-dashboard.conf 复制到 /etc/nginx/conf.d 目录
COPY pi-dashboard.conf /etc/nginx/conf.d/default.conf
