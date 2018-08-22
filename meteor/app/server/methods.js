/*****************************************************************************/
/*  Methods */
/*****************************************************************************/

import { Dags } from '../lib/collections/dags.js';
import { DagsVis } from '../lib/collections/dags.js';

Meteor.methods({
    'add_vis': function(id) {
        // Create a visualisation
        var thisID = new Mongo.ObjectID(id);
        // Get the configuration of this DAG
        dag = Dags.findOne({'_id':thisID});
        // Create a visualistion for this DAG
        return DagsVis.insert({
            "name": dag["dag_name"],
            "dag_id_str": id.str,
            "dag_id": id,
            "title": dag["vis_title"],
            "configuration": dag["vis_configuration"],
            "text": dag["vis_text"],
            "type": dag["vis_type"],
            "createdAt": dag["created_at"],
            "updatedAt": dag["updated_at"],
            "footer": dag["vis_footer"],
            "data": dag["clean_data"]
        });
    },
    'change_vis': function(id) {
        // Get the configuration of this DAG
        var thisID = new Mongo.ObjectID(id);
        // Get the configuration of this DAG
        dag = Dags.findOne({'_id':thisID});
        dagVis = DagsVis.findOne({'dag_id':id});
        // Update the visualistion for this DAG
        return DagsVis.update({
            '_id': dagVis._id
        }, {
            $set: {
                "name": dag["dag_name"],
                "dag_id_str": id.str,
                "dag_id": id,
                "title": dag["vis_title"],
                "configuration": dag["vis_configuration"],
                "text": dag["vis_text"],
                "type": dag["vis_type"],
                "createdAt": dag["created_at"],
                "updatedAt": dag["updated_at"],
                "footer": dag["vis_footer"],
                "data": dag["clean_data"]
            }
        });
    },
    'remove_vis': function(id) {
        // Delete a visualisation
        DagsVis.remove({
            "_id": id
        });
    }
});
