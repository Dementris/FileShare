
FROM node:22 As build

WORKDIR /usr/src/app

COPY package*.json package-lock.json ./

RUN npm ci

COPY ./ ./

RUN chmod +x /usr/src/app/start-nginx.sh

RUN npm run build


FROM nginx:stable-alpine as production

COPY --from=build /usr/src/app/nginx.conf /etc/nginx/conf.d

COPY --from=build /usr/src/app/dist /usr/share/nginx/html

COPY --from=build /usr/src/app/start-nginx.sh /usr/share/nginx/

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

RUN chmod +x /usr/share/nginx/start-nginx.sh

EXPOSE $PORT

ENTRYPOINT ["/usr/share/nginx/start-nginx.sh"]
