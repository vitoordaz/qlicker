#-*- coding: utf-8 -*-
'''
Created on 10.02.2011

@author: Victor Rodionov <vito.ordaz@gmail.com> 
'''
import os

from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile

class ResizeImageFieldFile(ImageFieldFile):    
    def save(self, name, content, save=True):
        super(ResizeImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)   
        img.thumbnail(
            (self.field.width, self.field.height),
            Image.ANTIALIAS
        )
        os.remove(self.path)#удаляем старый файл
        img.save(self.path, 'JPEG')
        
class ResizeImageField(ImageField):
    attr_class = ResizeImageFieldFile
    
    def __init__(self, new_width=128, new_height=128, *args, **kwargs):
        self.width = new_width
        self.height = new_height
        super(ResizeImageField, self).__init__(*args, **kwargs)