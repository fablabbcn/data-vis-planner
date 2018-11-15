![](homepage/img/datavisplanner_logo_100.png)


A platform for planning and scheduling data analyses and visualisations. Data analyses can then be configured in order to run periodically, and visualisations will be updated in realtime, and can be embedded everywhere on the web.

## Installation

The platform is organized with docker-compose, so the installation is quite simple:

- Clone the repo: ``git clone https://github.com/fablabbcn/DataVisPlanner.git``
- Go inside the project folder: ``cd DataVisPlanner``
- Customise the ``docker-compose.yml`` file if necessary
- Customise the ``environment.env`` and ``airflow.env`` files if necessary
- Customise the ``docker-compose.yml`` and ```mongo/mongo-init.js``` files for securing MongoDB where:
	- *MONGOADMINUSERNAME* is the admin username for MongoDB
	- *MONGOADMINPASSWORD* is the admin password for MongoDB
	- *MONGOUSERNAME* is the admin username for connecting Meteor with MongoDB
	- *MONGOPASSWORD* is the admin password for connecting Meteor with MongoDB
- Copy the ``environment.env`` to ``.env`` file
- Test the platform: ``docker-compose up --build``
- Run the platform: ``docker-compose up -d``

## Usage

The DataVisPlanner platform is based on several docker containers, only some of them need to be accessed directly. They can be accessed all from the homepage at **localhost:80**, here are the descriptions and links for direct access to the main containers (not all of them!):

- **Homepage** can be accessed at **localhost:80**, and from there all the important information and containers can be accessed
- Visualisations are rendered and listed with [Meteor](https://www.meteor.com/) at **localhost:3000**
- Data analyses processes are scheduled and maneged with [Airflow](https://airflow.incubator.apache.org/) at **localhost:8080**
- Data analyses processes can be written online with [Cloud9](https://c9.io/) at **localhost:8181**
- Data analyses processes using Celery can also be monitored with [Flower](http://flower.readthedocs.io/en/latest/) at **localhost:5555**
- Data stored in the Mongo database can be accessed with [Nosqlclient](https://www.nosqlclient.com/) at **localhost:3300**
- Data stored in the PostgreSQL database can be accessed with [pgAdmin](https://www.pgadmin.org/) at **localhost:5050**
- All the containers can be managed with [Portainer](https://portainer.io/) at **localhost:9000**

The homepage contains update instructions about how to use the platform and how to extend it with custom data analyses and visualisations. Please check the documentation of each container from their developers.

## Credits

[![](homepage/img/from_30.png)](https://ec.europa.eu/digital-agenda/en/news/22-new-caps-projects-horizon-2020)
