FROM node:4.0

# Updates and settings
RUN apt-get update && apt-get -y install sudo && apt-get install -y curl locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install Meteor
RUN curl https://install.meteor.com/ | sh

# Add non-root user
RUN useradd -m -G users -s /bin/bash meteoruser
RUN echo "user ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/user && chmod 0440 /etc/sudoers.d/user

# Copy the app
COPY . /home/meteoruser/.

# Change as root the permissions of the app
RUN chown -R meteoruser /home/meteoruser/

# Switch to non-root user, and run the app
USER meteoruser
WORKDIR /home/meteoruser/app/
RUN meteor --version
RUN meteor npm install
CMD meteor run