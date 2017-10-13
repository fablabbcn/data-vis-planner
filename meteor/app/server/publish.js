


Meteor.publish('dags', function () {
  return Dags.find();
});