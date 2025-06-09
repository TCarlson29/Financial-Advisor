
FROM node:18 AS frontend-build
WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci
RUN npm rebuild esbuild

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=frontend-build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
