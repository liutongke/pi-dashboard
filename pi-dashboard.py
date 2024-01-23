#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import socket


def get_os():
    os_name = platform.system()
    if os_name == "Windows":
        return True
    elif os_name == "Linux":
        return False


def windows():
    # 使用subprocess模块执行ipconfig命令，并使用findstr筛选包含"IPv4"的行
    result = subprocess.check_output("ipconfig | findstr /i \"IPv4\"", shell=True)

    # 将输出结果按换行符分割成列表
    lines = result.decode("gbk").split("\r\n")

    # 遍历列表，找到包含"IPv4"的行，并提取第16个字段
    for line in lines:
        if "IPv4" in line:
            myip = line.split()[15]
            break
    return myip


def linux():
    # 创建一个临时的套接字连接到公共 IP 地址
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


# 获取当前脚本所在目录
current_directory = os.path.dirname(os.path.realpath(__file__))

# 创建网络
subprocess.run(['docker', 'network', 'create', 'pi-dashboard-net'])

if get_os():
    ip = windows()
else:
    ip = linux()

print(f"本机的 IP 地址是：{ip}")

subprocess.run([
    'docker',
    'run',
    '--name', 'php1',
    "-e", f"MY_IP={ip}",
    '--network', 'pi-dashboard-php-v1',
    '--network-alias', 'pi-dashboard-php',
    "--restart=always",
    '-p' '9000:9000',
    '-v', f'{current_directory}:/var/www/html/',
    '-v', '/etc/hostname:/etc/hostname',
    '-d',
    'php:8.1.18-fpm'
])

# 构建 Docker 镜像
subprocess.run(['docker', 'build', '-t', 'pi-dashboard-nginx:v1', '.'], cwd=current_directory)

# 运行 Docker 容器
subprocess.run(
    [
        'docker',
        'run',
        '--name', 'pi-dashboard-nginx-v1',
        '--network', 'pi-dashboard-net',
        '--network-alias', 'pi-dashboard-nginx',
        '--restart', 'always',
        '-p', '80:80',
        '-v', f'{current_directory}:/usr/share/nginx/html',
        '-d',
        'pi-dashboard-nginx:v1'
    ])
