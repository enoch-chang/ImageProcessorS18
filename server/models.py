from pymodm import fields, MongoModel


class User(MongoModel):
        email = fields.EmailField(primary_key=True)
        name = fields.CharField()
        images = fields.ListField()
        pro_images = fields.ListField()

        def image_info(self):

                image_info = {
                        "images": self.images,
                        "filename": self.filename,
                        "image_id": self.image_id,
                        "filetype": self.filetype,
                        "time_stamp": self.timestamp,
                        "image_size": self.image_size,
                        "histograms": self.histograms
                }
                return image_info

        def pos_images_infomation(self):

                pro_images_info = {
                        "images": self.images,
                        "filename": self.filename,
                        "images_id": self.images_id,
                        "filetype": self.filetype,
                        "time_stamp": self.time_stamp,
                        "time_duration": self.time_duration,
                        "histograms": self.histograms
                }
                return pro_images_info
