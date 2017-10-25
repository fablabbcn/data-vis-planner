/*****************************************************************************/
/*  Publish collections */
/*****************************************************************************/

import { Dags } from '../lib/collections/dags.js';
import { DagsVis } from '../lib/collections/dags.js';

Meteor.publish('dags', function () {
  return Dags.find();
});

Meteor.publish('dagsvis', function () {
  return DagsVis.find();
});
