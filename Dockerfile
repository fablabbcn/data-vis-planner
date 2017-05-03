FROM node:4.0

# Updates and settings
RUN apt-get update && apt-get -y install sudo && apt-get install -y curl locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install Meteor
RUN curl https://install.meteor.com/ | sh

# Add non-root user, and add Meteor for her
RUN useradd -m -G users -s /bin/bash meteoruser
RUN echo "user ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/user && chmod 0440 /etc/sudoers.d/user
USER meteoruser
RUN meteor --version

# Copy the app
ONBUILD USER meteoruser
# ONBUILD RUN cd /home/meteoruser && mkdir -p app
ONBUILD COPY . /home/meteor/app/.

# Change as root the permissions of the app
ONBUILD USER root
ONBUILD RUN chown -R meteoruser /home/meteoruser/app/
ONBUILD RUN rm -R /home/meteor/app/.meteor/local/*

# Switch to non-root user, and run the app
ONBUILD USER meteoruser

CMD cd /home/meteoruser/app && meteor run