from pymodm import fields, MongoModel

class User(MongoModel):
        user_email = fields.EmailField(primary_key=True)
        #user_names = fields.ListField(field=fields.CharField())
        user_names = fields.CharField()
        user_ori_images = fields.ListField(field=fields.CharField())
        user_processed_images = fields.ListField(field=fields.CharField())
        user_ori_images_id = fields.ListField(field=fields.CharField())
        user_ori_images_time = fields.ListField(field=fields.DateTimeField())
        user_ori_images_filetype = fields.ListField(field=fields.CharField())
        user_images_his = fields.ListField(field=fields.CharField())
        user_images_contrast = fields.ListField(field=fields.CharField())
        user_images_log = fields.ListField(field=fields.CharField())
        user_images_reverse = fields.ListField(field=fields.CharField())
        user_images_pro_time = fields.ListField(field=fields.DateTimeField())

        def user_info(self):

                user_info = {
                        "user_email": self.user_email,
                        "user_names": self.user_names,
                        "user_ori_images": self.user_ori_images,
                        "user_processed_images": self.user_processed_images
                }
                return user_info

        def images_info(self):

                images_info = {
                        "user_ori_images": self.user_ori_images,
                        "images_id": self.user_ori_images_id,
                        "images_time": self.user_ori_images_time
                }
                return images_info

        def proimages_info(self):

                proimages_info = {
                        "user_ori_images": self.user_ori_images,
                        "images_id": self.user_ori_images_id,
                        "images_pro_his": self.user_images_his,
                        "images_pro_log": self.user_images_log,
                        "images_pro_con": self.user_images_contrast,
                        "images_pro_rev": self.user_images_reverse
                }
                return proimages_info