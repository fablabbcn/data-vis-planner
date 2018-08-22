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

    var d3 = Plotly.d3;

    // 10% margin
    var WIDTH_IN_PERCENT_OF_PARENT = 90,
        HEIGHT_IN_PERCENT_OF_PARENT = 90;

    // Add the vis div with the specific size
    var gd3 = d3.select('#vis-div')
        .append('div')
        .style({
            width: WIDTH_IN_PERCENT_OF_PARENT + '%',
            'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

            height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh',
            'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + 'vh'
        });
    var gd = gd3.node();

    // Override or fix any font configuration
    this.data.configuration.font = {
        'family': 'Fira Sans, sans-serif',
        'size': 18,
        'font-weight': 600,
        'color': '#000'
    }
    // Plot the data
    Plotly.plot(gd, [this.data.data], this.data.configuration);
    // Resize the data on window resize
    window.onresize = function() {
        Plotly.Plots.resize(gd);
    };
});

Template.Vis.onDestroyed(function() {});
