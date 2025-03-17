FROM node:18-slim

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json /app/
RUN npm install

COPY frontend /app

RUN npm run build

RUN npm install -g serve

EXPOSE 5000

CMD ["serve", "-s", "dist", "-l", "5000"]
