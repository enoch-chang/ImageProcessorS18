from pymodm import fields, MongoModel

class User(MongoModel):
        email = fields.EmailField(primary_key=True)
        #user_names = fields.ListField(field=fields.CharField())
        name = fields.CharField()
        images = fields.DictField()
        pro_images = fields.DictField()
        #images_info = fields.ListField()
        #pro_images_info = fields.ListField()
        #user_ori_images_id = fields.ListField(field=fields.CharField())
        #user_ori_images_time = fields.ListField(field=fields.DateTimeField())
        #user_ori_images_filetype = fields.ListField(field=fields.CharField())
        #user_images_pro_time = fields.ListField(field=fields.DateTimeField())
        #image_pro_type = fields.CharField()

        def user_info(self):

                user_info = {
                        "email": self.email,
                        "name": self.name,
                        "images": self.images,
                        "pro_images": self.pro_images
                }
                return user_info

        def images_infomation(self):

                images_infomation = {
                        "images": self.images,
                        "images_id": self.user_ori_images_id,
                        "images_time": self.user_ori_images_time
                }
                return images_infomation
