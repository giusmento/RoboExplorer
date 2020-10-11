# build environment
FROM node:13.12.0-alpine as build
WORKDIR /
ENV PATH node_modules/.bin:$PATH

#RUN npm ci --silent
#RUN npm install react-scripts@3.4.1 -g --silent
COPY . ./app
COPY package.json ./app
WORKDIR /app
RUN npm install
RUN npm run build

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]