db.auth('MONGOADMINUSERNAME', 'MONGOADMINPASSWORD')

db = db.getSiblingDB('meteor')

db.createUser({
  user: 'MONGOUSERNAME',
  pwd: 'MONGOPASSWORD',
  roles: [
    {
      role: 'readWrite',
      db: 'meteor',
    },
  ],
});
