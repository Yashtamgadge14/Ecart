from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
    CAT=((1,'mobile'),(2,'footwear'),(3,'clothing'))
    name=models.CharField(max_length=50,verbose_name='product name')
    price=models.FloatField()
    pdetails=models.CharField(max_length=100,verbose_name='product details')
    category=models.IntegerField(verbose_name='category',choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="available")
    pimage=models.ImageField(upload_to='image')
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column='pid')
    qty=models.BigIntegerField(default=1)

class order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column='pid')
    qty=models.BigIntegerField(default=1)
