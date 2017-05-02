FROM node:4.0

# Updates and settings
RUN apt-get update && apt-get -y install sudo && apt-get install -y curl locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install Meteor
RUN curl https://install.meteor.com/ | sh
ENV INSTALL_PATH /meteor
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

# Copy and run app
COPY . .
RUN cd app/;meteor npm install --production
CMD cd app;meteor --allow-superuser
