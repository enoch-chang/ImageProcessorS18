from pymodm import fields, MongoModel


class User(MongoModel):
        """
        This MongoModel store the data into database.
        :param email: EmailField to store user emails
        :param name: CharField to store user names
        :param images: ListField to store original images
        with their information including the base64 str of the images,
        filename, id, filetype, time stamp, image size and unaltered
        histograms.
        :param pro_images: ListField to store processed images
        with their information including base64 str of the images, filename,
        id, process type, time stamp, time duration and processed histograms.
        """
        email = fields.EmailField(primary_key=True)
        name = fields.CharField()
        images = fields.ListField()
        pro_images = fields.ListField()