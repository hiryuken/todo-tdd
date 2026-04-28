# ── Frontend — nginx ──────────────────────────────────────────────────────────
# Serve i file statici e fa da reverse proxy verso il backend Flask.
# Questo elimina il CORS: il browser parla solo con nginx su :3000,
# nginx gira /api/* al backend sulla rete interna Docker.

FROM nginx:1.27-alpine

# Rimuovi la config di default nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia la configurazione nginx
COPY nginx.conf /etc/nginx/conf.d/todo.conf

# Copia i file statici
COPY src/ /usr/share/nginx/html/

# Sovrascrive config.js con la versione Docker (API_BASE = "/api")
COPY src/config.docker.js /usr/share/nginx/html/config.js

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
