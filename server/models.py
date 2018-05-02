from pymodm import fields, MongoModel


class User(MongoModel):
        email = fields.EmailField(primary_key=True)
        name = fields.CharField()
        images = fields.ListField()
        pro_images = fields.ListField()

