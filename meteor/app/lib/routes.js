import { DagsVis } from './collections/dags.js'

Router.configure({
    layoutTemplate: 'MasterLayout',
    loadingTemplate: 'Loading',
    notFoundTemplate: 'NotFound'
});

Router.route('/', function() {
    this.render('Home');
});

Router.route('/vis/:_id', function() {
    this.wait(Meteor.subscribe('dagsvis', this.params._id));
    if (this.ready()) {
        this.render('Vis', {
            data: function() {
                return DagsVis.findOne({
                    _id: this.params._id
                });
            }
        });
    } else {
        this.render('Loading');
    }
});
