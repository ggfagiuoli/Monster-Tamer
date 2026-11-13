
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:0
ENV QT_QPA_PLATFORM=xcb
ENV SCREEN_WIDTH=1280
ENV SCREEN_HEIGHT=800
ENV SCREEN_DEPTH=24

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    openbox \
    x11-utils \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libx11-xcb1 \
    libxcb1 \
    libegl1 \
    libgl1 \
    libfontconfig1 \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libxi6 \
    libdbus-1-3 \
    libglib2.0-0 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# noVNC web interface
EXPOSE 6080

# Start virtual display, window manager, VNC and application
CMD ["sh", "-c", "\
    Xvfb :0 -screen 0 ${SCREEN_WIDTH}x${SCREEN_HEIGHT}x${SCREEN_DEPTH} -ac & \
    sleep 2 && \
    openbox & \
    sleep 2 && \
    x11vnc -display :0 -forever -shared -nopw -listen localhost -rfbport 5900 & \
    sleep 2 && \
    websockify --web=/usr/share/novnc/ 6080 localhost:5900 & \
    sleep 2 && \
    exec python main.py \
"]