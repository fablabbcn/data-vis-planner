import { DagsVis } from './collections/dags.js'

Router.configure({
  layoutTemplate: 'MasterLayout',
  loadingTemplate: 'Loading',
  notFoundTemplate: 'NotFound'
});


Router.route('/', function () {
  this.render('Home');
});

Router.route('vis/:_id', {
    name: 'vis',
    controller: 'VisController',
    data: function(){
        return DagsVis.findOne({ _id: this.params._id });
    },
    where: 'client'
});
