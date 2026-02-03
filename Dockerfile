# 使用 Node.js 作為基礎鏡像 (Debian-based)
FROM node:20-slim

# 安裝 Python 及其編譯所需的系統依賴
# build-essential, python3-dev 是安裝某些 Python 套件 (如 bcrypt, pandas) 時編譯需要的
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libffi-dev \
    procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製後端與前端的設定檔案
COPY backend/requirements.txt ./backend/
COPY frontend/package*.json ./frontend/

# 更新 pip 並安裝依賴
# 使用 --break-system-packages 是因為 Debian 12 核心環境保護，容器內建議直接使用# 更新 pip 並安裝依賴
RUN pip3 install --no-cache-dir --upgrade pip --break-system-packages --root-user-action=ignore && \
    pip3 install --no-cache-dir -r backend/requirements.txt --break-system-packages --root-user-action=ignore

# 安裝前端依賴
RUN cd frontend && npm install

# 複製其餘專案檔案
COPY . .

# 修正 Windows 換行符號問題
RUN tr -d '\r' < start.sh > start_unix.sh && mv start_unix.sh start.sh
RUN chmod +x start.sh

# 曝露端口 (Express 代理後端)
EXPOSE 3000

# 啟動命令
CMD ["bash", "start.sh"]
