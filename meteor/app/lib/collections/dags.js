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

// Check that there are no existing dagsvis for the same dag already existing
existingDagsVis2 = DagsVis.find();
console.log("DEBUG12": existingDagsVis2);

// import { Dags } from '../lib/collections/dags.js';
// import { DagsVis } from '../lib/collections/dags.js';

// Listen for changes in the Airflow DAGs collections in order manage visualisations
var cursor = Dags.find();
cursor.observeChanges({
    added: function(id, fields) {
        // A new data source from DAGs was added
        console.log("A new DAGs data source was created in Mongo with id:", id._str);
        // Check that there are no existing dagsvis for the same dag already existing
        existingDagsVis = DagsVis.find({
            "dag_id": id._str
        }, { fields: { "dag_id": 1 }});
        existingDagsVis2 = DagsVis.find({}, { sort: { createdAt: -1 } });

        console.log("DEBUG1": existingDagsVis);
        console.log("DEBUG12": existingDagsVis2);
        console.log("DEBUG2": existingDagsVis._docs._map);

        if (_.isEmpty(existingDagsVis)) {
            console.log(existingDagsVis);
        } else {
            // Create a visualisation
            Meteor.call('add_vis', id, function(error, result) {
                if (error) {
                    console.log("Error in adding a visualisation:", error, "ID:", id._str);
                } else {
                    console.log("A new DAGs data vis was created with id:", result);
                }
            });
        }
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
            }
        });
    }
});
