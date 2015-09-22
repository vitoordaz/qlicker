import os

import PIL

from django.db.models.fields import files


class ResizeImageFieldFile(files.ImageFieldFile):
    def save(self, name, content, save=True):
        super(ResizeImageFieldFile, self).save(name, content, save)
        img = PIL.Image.open(self.path)
        img.thumbnail((self.field.width, self.field.height),
                      PIL.Image.ANTIALIAS)
        os.remove(self.path)  # remove old file
        img.save(self.path, 'JPEG')


class ResizeImageField(files.ImageField):
    attr_class = ResizeImageFieldFile

    def __init__(self, new_width=128, new_height=128, *args, **kwargs):
        self.width = new_width
        self.height = new_height
        super(ResizeImageField, self).__init__(*args, **kwargs)
