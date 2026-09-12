FROM node:22-bookworm AS web
WORKDIR /src/web
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000
COPY requirements.txt pyproject.toml ./
COPY engine ./engine
COPY backend ./backend
COPY knowledge ./knowledge
COPY app.py ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=web /src/web/dist ./web/dist
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
