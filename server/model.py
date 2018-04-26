from pymodm import fields, MongoModel

class User(MongoModel):
        user_email = fields.EmailField(primary_key=True)
        user_names = fields.CharField()
        user_ori_images = fields.ListField(field=fields.CharField())
        user_processed_images = fields.ListField(field=fields.CharField())
        user_ori_images_filename = fields.CharField()
        user_ori_images_time = fields.DateTimeField()
        user_images_his = fields.ListField(field=fields.CharField())
        user_images_contrast = fields.ListField(field=fields.CharField())
        user_images_log = fields.ListField(field=fields.CharField())
        user_images_reverse = fields.ListField(field=fields.CharField())
        user_images_pro_time = fields.DateTimeField()
