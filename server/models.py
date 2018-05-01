from pymodm import fields, MongoModel


class User(MongoModel):
        email = fields.EmailField(primary_key=True)
        name = fields.CharField()
        images = fields.ListField()
        pro_images = fields.ListField()

        def image_info(self):

                user_info = {
                        "images": self.images,
                        "filename": self.filename,
                        "image_id": self.image_id,
                        "pro_images": self.pro_images
                }
                return user_info

        def pos_images_infomation(self):

                images_infomation = {
                        "images": self.images,
                        "images_id": self.user_ori_images_id,
                        "images_time": self.user_ori_images_time
                }
                return images_infomation
