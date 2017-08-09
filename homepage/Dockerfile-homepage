# https://hub.docker.com/_/nginx/

FROM nginx:alpine

RUN apk --update add git nodejs && rm -rf /var/cache/apk/* && \
    npm install -g yarn grunt-cli && \
    echo '{ "allow_root": true }' > /root/.bowerrc

COPY . /usr/share/nginx/html

WORKDIR /usr/share/nginx/html

RUN yarn install
