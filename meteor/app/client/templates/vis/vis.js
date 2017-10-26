/*****************************************************************************/
/* Vis: Event Handlers */
/*****************************************************************************/
Template.Vis.events({});

/*****************************************************************************/
/* Vis: Helpers */
/*****************************************************************************/
Template.Vis.helpers({
    data: function() {
        return this;
    }
});

/*****************************************************************************/
/* Vis: Lifecycle Hooks */
/*****************************************************************************/
Template.Vis.onCreated(function() {
    this.subscribe("dagsvis");
});

Template.Vis.onRendered(function() {

    console.log("Data:", this.data);
    var label = "number of labs";
    var value = this.data.data["number of labs"];

    const data = [{
        x: [label],
        y: [value],
        type: 'bar'
    }];
    const settings = {
        margin: {
            t: 0
        }
    };
    Plotly.plot($('#visdiv')[0], data, settings);
});

Template.Vis.onDestroyed(function() {});
