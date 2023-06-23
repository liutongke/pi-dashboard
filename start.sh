#!/bin/bash

#创建bridge网络
docker network create pi-dashboard-net

#创建nginx
sudo docker run --name nginx1 --network pi-dashboard-net --network-alias pi-dashboard-nginx --restart always -p 80:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx

hostip=$(hostname -I | awk '{print $1}')
echo $hostip
#创建php（绑定宿主机名称让容器内可或者正确hostname）-e MY_IP绑定宿主机ip
sudo docker run --name php1 -e MY_IP="$hostip" --network pi-dashboard-net --network-alias pi-dashboard-php --restart always -p 9000:9000 -v /var/www/html:/var/www/html -v /etc/hostname:/etc/hostname -d php:8.1.18-fpm
