from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import os
import urllib
from django.core.files import File
from django.db import models
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

# Create your models here.
class Organizations(models.Model):
    name_ar = models.CharField(max_length=500,blank=True, null=True)
    name_en = models.CharField(max_length=500,blank=True, null=True)
    logo = models.ImageField(upload_to='uploads/')
    city = models.CharField(max_length=300,blank=True, null=True)
    phone = models.CharField(max_length=300,blank=True, null=True)
    website = models.CharField(max_length=300,blank=True, null=True)
    device_id = models.CharField(max_length=300,blank=True, null=True)
    charity_id = models.CharField(max_length=500,blank=True, null=True)
    class Meta:
        verbose_name_plural = "Organizations"
    def __str__(self):
        return self.name_ar

    def get_remote_image(self , url):
        #result = urllib.request.urlretrieve(url)
        #print("file:" ,result[0])
        #self.logo.save( os.path.basename(url), File(open(result[0])) )
        #self.save()
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        self.logo.save(f"image_logo.png", File(img_temp))
        self.save()
    

class Types(models.Model):
    type_ar = models.CharField(max_length=100,blank=True, null=True)
    type_en = models.CharField(max_length=100,blank=True, null=True)
    charity_id = models.CharField(max_length=300,blank=True, null=True)
    type_id = models.CharField(max_length=300,blank=True, null=True)
    #added by zahraa
    _id = models.CharField(max_length=300,blank=True, null=True)
   
    
    class Meta:
        verbose_name_plural = "Zakah types"
    def __str__(self):
        return self.type_ar


class Sub_types(models.Model):
    sub_type_ar = models.CharField(max_length=300,blank=True, null=True)
    sub_type_en = models.CharField(max_length=300,blank=True, null=True)
    sub_id = models.CharField(max_length=300,blank=True, null=True)
    type_id = models.CharField(max_length=300,blank=True, null=True)
        
    class Meta:
        verbose_name_plural = "Sub Zakah types"
    def __str__(self):
        return self.sub_type_ar

class Transaction(models.Model):
    type = models.CharField(max_length=500,blank=True, null=True)
    money= models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.datetime.now())
    device_id = models.CharField(max_length=300,blank=True, null=True)
    trans_id = models.CharField(max_length=300,blank=True, null=True)
    class Meta:
        verbose_name_plural = "Donate Transaction"
    def __str__(self):
        return self.type
   
    