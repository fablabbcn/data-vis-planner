//var database = new MongoInternals.RemoteCollectionDriver("mongodb://mongo:27017/dags");
//Dags = new Mongo.Collection('dags', { _driver: database });


// DAGs created by Airflow
Dags = new Mongo.Collection('dags');

if (Meteor.isServer) {
  Dags.allow({
    insert: function (userId, doc) {
      return false;
    },

    update: function (userId, doc, fieldNames, modifier) {
      return false;
    },

    remove: function (userId, doc) {
      return false;
    }
  });

  Dags.deny({
    insert: function (userId, doc) {
      return true;
    },

    update: function (userId, doc, fieldNames, modifier) {
      return true;
    },

    remove: function (userId, doc) {
      return true;
    }
  });
}


// Meteor visualisations based on the Airflow DAGs
DagsVis = new Mongo.Collection('dags');

if (Meteor.isServer) {
  DagsVis.allow({
    insert: function (userId, doc) {
      return false;
    },

    update: function (userId, doc, fieldNames, modifier) {
      return false;
    },

    remove: function (userId, doc) {
      return false;
    }
  });

  DagsVis.deny({
    insert: function (userId, doc) {
      return true;
    },

    update: function (userId, doc, fieldNames, modifier) {
      return true;
    },

    remove: function (userId, doc) {
      return true;
    }
  });
}

// Listen for changes in the Airflow DAGs collections in order manage visualisations
var cursor = Dags.find();
cursor.observeChanges({
    added: function(id, fields) {
        console.log("ADDED:", id);
    },
    changed: function(id, fields) {
        console.log("CHANGED:", id);
    },
    removed: function(id) {
        console.log("REMOVED:", id);
    }
});
