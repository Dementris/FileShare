
FROM node:22 As build

WORKDIR /usr/src/app

COPY package*.json package-lock.json ./

RUN npm ci

COPY ./ ./

RUN npm run build


FROM nginx:stable-alpine as production

COPY --from=build /usr/src/app/nginx.conf /etc/nginx/conf.d

COPY --from=build /usr/src/app/dist /usr/share/nginx/html

COPY --from=build /usr/src/app/start-nginx.sh /usr/share/nginx/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
