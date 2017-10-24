Router.configure({
  layoutTemplate: 'MasterLayout',
  loadingTemplate: 'Loading',
  notFoundTemplate: 'NotFound'
});


Router.route('/', {
  name: 'home',
  controller: 'HomeController',
  where: 'client'
});

Router.route('vis/:_id', {
    name: 'vis',
    controller: 'VisController',
    data: function(){
        return DagsVis.findOne({ _id: this.params._id });
    },
    where: 'client'
});
