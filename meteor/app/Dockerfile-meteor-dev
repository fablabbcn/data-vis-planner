FROM node:4.0


RUN apt-get update && apt-get install -y curl locales locales-all

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN curl https://install.meteor.com/ | sh

ENV INSTALL_PATH /meteor


RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY . .

RUN meteor npm install
CMD meteor --allow-superuser
