/*****************************************************************************/
/*  Publish collections */
/*****************************************************************************/


Meteor.publish('dags', function () {
  return Dags.find();
});

Meteor.publish('dagsvis', function () {
  return DagsVis.find();
});
