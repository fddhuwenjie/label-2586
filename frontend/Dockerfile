# -*- coding: utf-8 -*-
# Dockerfile for Text Adventure Game
# 支持 ARM 和 X86 架构的跨平台镜像，带 noVNC 支持

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DISPLAY=:99

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Pygame 依赖
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    # 中文字体
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    # X11 虚拟帧缓冲
    xvfb \
    x11vnc \
    # noVNC
    novnc \
    websockify \
    # 窗口管理器
    fluxbox \
    # 工具
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 配置 fluxbox 隐藏窗口装饰
RUN mkdir -p /root/.fluxbox
COPY fluxbox_apps /root/.fluxbox/apps
COPY fluxbox_init /root/.fluxbox/init

# 替换 noVNC 默认首页
COPY novnc_index.html /usr/share/novnc/index.html

# 复制 supervisor 配置
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 暴露 noVNC 端口
EXPOSE 6080

# 启动 supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
