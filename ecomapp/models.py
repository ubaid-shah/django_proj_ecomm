from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# means adding coloumns to tables 
            #module #class
class Product(models.Model):
    CAT=((1,'Mobiles'),(2,'Shoes'),(3,'Cloth'))
    name=models.CharField(max_length=20,verbose_name='Product Name')
    price=models.IntegerField()
    pdetail=models.CharField(max_length=300,verbose_name='Product Details')
    cat=models.IntegerField(verbose_name='Category')
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='image')

    def __str__(self):
        return self.name
class Cart(models.Model):
    uid_id=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid_id')
    pid_id=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid_id')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    uid_id=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid_id')
    pid_id=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid_id')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()
