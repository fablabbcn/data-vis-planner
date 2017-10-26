/*****************************************************************************/
/* TabularButtons: Event Handlers */
/*****************************************************************************/
Template.TabularButtons.events({
});

/*****************************************************************************/
/* TabularButtons: Helpers */
/*****************************************************************************/
Template.TabularButtons.helpers({
    data: function() {
        return window.location.href + "vis/" + this._id;
    },
});

/*****************************************************************************/
/* TabularButtons: Lifecycle Hooks */
/*****************************************************************************/
Template.TabularButtons.onCreated(function () {
});

Template.TabularButtons.onRendered(function () {
});

Template.TabularButtons.onDestroyed(function () {
});
