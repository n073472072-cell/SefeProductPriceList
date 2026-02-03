# 使用 Node.js 作為基礎鏡像
FROM node:20-slim

# 安裝 Python 及其依賴環境
RUN apt-get update && apt-get install -y python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製後端與前端的設定檔案
COPY backend/requirements.txt ./backend/
COPY frontend/package*.json ./frontend/

# 安裝依賴 (使用 --break-system-packages 因為在容器內是安全的)
RUN pip3 install --no-cache-dir -r backend/requirements.txt --break-system-packages
RUN cd frontend && npm install

# 複製其餘專案檔案
COPY . .

# 曝露端口 (Zeabur 會自動對應首個曝露或使用的端口)
EXPOSE 3000
EXPOSE 8000

# 啟動命令
CMD ["bash", "start.sh"]
