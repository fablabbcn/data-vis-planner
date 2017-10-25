// var database = new MongoInternals.RemoteCollectionDriver("mongodb://mongo:27017/dags");
// export const Dags = new Mongo.Collection('dags', { _driver: database });


// DAGs created by Airflow
export const Dags = new Mongo.Collection('dags');

if (Meteor.isServer) {
    Dags.allow({
        insert: function(userId, doc) {
            return false;
        },

        update: function(userId, doc, fieldNames, modifier) {
            return false;
        },

        remove: function(userId, doc) {
            return false;
        }
    });

    Dags.deny({
        insert: function(userId, doc) {
            return true;
        },

        update: function(userId, doc, fieldNames, modifier) {
            return true;
        },

        remove: function(userId, doc) {
            return true;
        }
    });
}


// Meteor visualisations based on the Airflow DAGs
export const DagsVis = new Mongo.Collection('dagsvis');

if (Meteor.isServer) {
    DagsVis.allow({
        insert: function(userId, doc) {
            return false;
        },

        update: function(userId, doc, fieldNames, modifier) {
            return false;
        },

        remove: function(userId, doc) {
            return false;
        }
    });

    DagsVis.deny({
        insert: function(userId, doc) {
            return true;
        },

        update: function(userId, doc, fieldNames, modifier) {
            return true;
        },

        remove: function(userId, doc) {
            return true;
        }
    });
}

// Listen for changes in the Airflow DAGs collections in order manage visualisations
var cursor = Dags.find();
cursor.observeChanges({
    added: function(id, fields) {
        // A new data source from DAGs was added
        console.log("A new DAGs data source was created in Mongo with id:", id._str);
        // Create a visualisation
        Meteor.call('add_vis', id, function(error, result) {
            if (error) {
                console.log("Error in adding a visualisation:", error, "ID:", id._str);
            } else {
                console.log("A new DAGs data vis was created with id:", result);
                Router.go('vis', {
                    _id: result
                });
            }
        });
    },
    changed: function(id, fields) {
        // An existing data source from DAGs was edited
        console.log("An existing DAGs data source was edited in Mongo with id:", id._str);
        // Edit a visualisation
        Meteor.call('change_vis', id, function(error, result) {
            if (error) {
                console.log("Error in editing a visualisation:", error, "ID:", id._str);
            } else {
                console.log("An existing DAGs data vis was edited with id:", result);
                Router.go('vis', {
                    _id: result
                });
            }
        });
    },
    removed: function(id) {
        // An existing data source from DAGs was deleted
        console.log("An existing DAGs data source was deleted in Mongo with id:", id._str);
        // Delete a visualisation
        Meteor.call('remove_vis', id, function(error, result) {
            if (error) {
                console.log("Error in deleting a visualisation:", error, "ID:", id._str);
            } else {
                console.log("An existing DAGs data vis was deleted with id:", result);
                Router.go('home');
            }
        });
    }
});
