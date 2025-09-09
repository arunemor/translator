FROM python:3.11-bookworm

# Install PyQt5 runtime deps including xcb plugin deps
RUN apt-get update && apt-get install -y \
    libx11-xcb1 libxrender1 libxcb1 libxext6 \
    libxcb-render0 libxcb-shape0 libxcb-xfixes0 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
    libxcb-randr0 libxcb-render-util0 libxcb-shm0 \
    libxcb-util1 libxcb-xinerama0 libxcb-xkb1 \
    libxkbcommon0 libxkbcommon-x11-0 \
    libgl1 libglx-mesa0 mesa-utils \
    xclip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
