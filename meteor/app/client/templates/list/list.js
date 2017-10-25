/*****************************************************************************/
/* List: Event Handlers */
/*****************************************************************************/
Template.List.events({
});

/*****************************************************************************/
/* List: Helpers */
/*****************************************************************************/
Template.List.helpers({
    allVis: function() {
        return DagsVis.find();
    },
});

/*****************************************************************************/
/* List: Lifecycle Hooks */
/*****************************************************************************/
Template.List.onCreated(function () {
    self.subscription = Meteor.subscribe('dags');
    self.subscription = Meteor.subscribe('dagsvis');
});

Template.List.onRendered(function () {
});

Template.List.onDestroyed(function () {
});

// Setup of tabular for this template
import { $ } from 'meteor/jquery';
import dataTablesBootstrap from 'datatables.net-bs';
import 'datatables.net-bs/css/dataTables.bootstrap.css';
dataTablesBootstrap(window, $);
