from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#
#class Buyer(models.Model):
#    BuyerID = models.CharField(max_length = 100, primary_key = True)
#    Username = models.CharField(max_length = 100, unique = True)
#    Userr = models.ForeignKey(User,unique = True)
#    Password = models.CharField(max_length = 128)
#    Phone = models.CharField(max_length = 11, unique = True)
#    Email = models.CharField(max_length = 100)
#    Activatestate = models.CharField(max_length = 10)
#class BuyerAddrInfo(models.Model):
#    BuyerAddr = models.CharField(max_length = 100)
#    BuyerPhone = models.CharField(max_length = 11)
#    Buyername = models.CharField(max_length = 100)
#    Postcode = models.CharField(max_length = 10)
#    City = models.CharField(max_length = 10)
#    Buyer= models.ForeignKey(Buyer)
#    
#class Admin(models.Model):
#    Userin = models.ForeignKey(User,unique = True)
#    Adminname = models.CharField(max_length = 100, unique = True)
#    AdminPasswd = models.CharField(max_length = 128)
#
#class Catalog(models.Model):
#    CateID = models.CharField(max_length = 100,primary_key = True)
#    Catename = models.CharField(max_length = 100)    
#
#    
#class Goods(models.Model):
#    GoodsID = models.CharField(max_length = 100, primary_key = True)
#    Goodsname = models.CharField(max_length = 100)
#    Cate = models.ForeignKey(Catalog)
#    Picture = models.CharField(max_length = 100)
#    Price = models.CharField(max_length = 20)
#    StockQua = models.CharField(max_length = 20)
#    Info = models.CharField(max_length = 1000)
#
#class OrderItem(models.Model):
#    ItemID = models.CharField(max_length = 100, primary_key = True)
#    GoodsID = models.CharField(max_length = 100)
#    Goodsname = models.CharField(max_length = 100)
#    Price = models.CharField(max_length = 20)
#    Picture = models.CharField(max_length = 100)
#    Quantity = models.CharField(max_length = 5)
#
#class Order(models.Model):
#    OrderID = models.CharField(max_length = 100, primary_key = True)
#    OrderItems = models.ManyToManyField(OrderItem)
#    User = models.ForeignKey(BuyerAddrInfo)
#    OrderTime = models.CharField(max_length = 50)
#    TotalPrice = models.CharField(max_length = 100)
#    Orderstate = models.CharField(max_length = 20)
#
#class Cart(models.Model):
#    buyer = models.ForeignKey(Buyer)
#    item= models.ForeignKey(OrderItem)
#        
