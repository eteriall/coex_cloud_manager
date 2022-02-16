from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields


class Server(MongoModel):
    yc_id = fields.CharField()
    ip = fields.CharField()
    access_code = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'coex-cloud'


class User(MongoModel):
    name = fields.CharField()
    auth_code = fields.CharField(primary_key=True)
    first_name = fields.CharField()
    last_name = fields.CharField()


    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'coex-cloud'
