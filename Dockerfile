FROM node:20.0.0-alpine AS build
WORKDIR /weblog
COPY . .
RUN yarn
RUN yarn build

FROM nginx:1.23.4-alpine AS deploy-static
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /weblog/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
