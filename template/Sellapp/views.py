# -*- coding:UTF-8 -*-
import time
import random
import MySQLdb
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
#from Sellapp.models import Buyer,BuyerAddrInfo,Admin,Catalog,Goods,OrderItem,Order,Cart
from Sellapp.sql import mysql_init
try:
    mysql_init()
except:
    pass
HOMEPAGE_URL = "http://127.0.0.1:8000/"
def homepage(request):
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    user_flag = False
    admin_flag = False
    userid = request.user.id
    n = cursor.execute("select * from Buyer where id = %s",[userid])
    if n != 0:
        buyer = cursor.fetchall()    
        user_flag = True
        username = request.user.username
    else:
        n = cursor.execute("select * from Admin where id = %s",[userid])
        if n != 0:
            admin = cursor.fetchall()  
            admin_flag = True
            adminname = request.user.username
        else:
            user_flag = False
#    except:
#        user_flag = False
    n = cursor.execute("select * from Allkind") 
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    if request.POST:
        post = request.POST
        if "submit" in post:
            if "s" in post:
                goodsname = post["s"]
                n = cursor.execute("select GoodsID from Goodsshort where Goodsname = %s",[goodsname]) 
                goodsid = cursor.fetchall()[0][0]
                return HttpResponseRedirect(HOMEPAGE_URL + 'proinfo/' + goodsid +'/') 
    cursor.close()    
    conn.close()   
    return render_to_response('index.html',locals())
    

def register(request):
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind")  
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    error = []
    if request.POST:
        post = request.POST
        bid = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + str(random.randrange(1000,9999))
#        if not password:
#            error.append("请输入密码")
#            return render_to_response('register.html',locals())
 #--Decrypt the key_encrypted--#
       
        username  = post["username"]
        email= post["email"]
        phone = post["phone"]
        password = post["password"]
        try:
            userb = User.objects.create_user(username =username,password = password)
            nid = userb.id
                # ------------------------send email---------------------------------------------
            sql = "insert into Buyer(BuyerID,Username,Password,id,Phone,Email) values(%s,%s,%s,%s,%s,%s)"   
            n = cursor.execute(sql,[bid,username,password,nid,phone,email])  
            cursor.close()  
            conn.commit()
            conn.close()
        except:
            error.append("此用户名已存在！")
       
    return render_to_response('register.html',locals())

def login(request):
    error = []
    admin_flag = False
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind")  
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    if request.POST:
        post = request.POST
        try:
            userb = User.objects.get(username = post["username"])
            n = cursor.execute("select Password from Buyer where Username = %s",[userb.username]) 
            if n != 0:
                passwd = cursor.fetchall()[0][0] 
                password = post["password"]
                if(passwd == password):
                    user = auth.authenticate(username=post["username"], password=passwd)
                    auth.login(request,user)
                    return HttpResponseRedirect(HOMEPAGE_URL)
                else:
                    error.append("密码错误")
            else:  
                error.append("1")
                n = cursor.execute("select AdminPasswd from Admin where Adminname = %s",[userb.username]) 
                if n != 0:
                    admin_flag = True
                    adminname = request.user.username
                    passwd = cursor.fetchall()[0][0] 
                    password = post["password"]
                    if(passwd == password):
                        user = auth.authenticate(username=post["username"], password=passwd)
                        auth.login(request,user)
                        return render_to_response('index.html',locals())
                    else:
                        error.append("密码错误")
        except:
            error.append("用户名错误！")
    cursor.close()    
    conn.close()    
    return render_to_response('login.html',locals())
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(HOMEPAGE_URL)

class temp_checkaccount:
    OrderID = None
    TotalPrice = None
    Orderstate = None
    
    def __init__(self,OrderID,TotalPrice,Orderstate):
        self.OrderID = OrderID
        self.TotalPrice = TotalPrice
        self.Orderstate = Orderstate

def checkaccount(request):
    addr_flag = False
    user_flag = False
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind")  
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    try:
        userid = User.objects.get(username=request.user.username).id
        n = cursor.execute("select BuyerID from Buyer where id = %s",[userid])    
        buyerid = cursor.fetchall()[0][0]    
        user_flag = True
        username = request.user.username
        sql = "select OrderID,TotalPrice,Orderstate from BuyerOrder where BuyerID = %s and Orderstate = %s"
        cursor.execute(sql,[buyerid,"not payed"])
        or_notpay = []
        for temp in cursor.fetchall():
            or_notpay.append(temp_checkaccount(temp[0],temp[1],temp[2]))
        or_finish = []
        cursor.execute(sql,[buyerid,"finish"])
        for temp in cursor.fetchall():
            or_finish.append(temp_checkaccount(temp[0],temp[1],temp[2]))
    except:
        user_flag = False
       # return HttpResponseRedirect(HOMEPAGE_URL)
    
    n = cursor.execute("select * from BuyerAddrInfo where BuyerID = %s",[buyerid]) 
    if n != 0:
        addr_flag = True
        temp = cursor.fetchall()
        buyername = temp[0][3]
        buyerphone = temp[0][2]
        postcode = temp[0][4]
        buyeraddr = temp[0][1]
        city = temp[0][5]
    else:
        addr_flag = False
    
    if request.POST:
        post = request.POST
        for order in or_notpay:
            if (order.OrderID + "_cancel") in post:
                sql = "delete from Order_GoodsItem where OrderID=%s"
                n = cursor.execute(sql,[order.OrderID]) 
                sql = "delete from BuyerOrder where OrderID = %s"   
                n = cursor.execute(sql,[order.OrderID]) 
                #Order.objects.get(OrderID = order.OrderID).delete()
        for order in or_finish:
            if (order.OrderID + "_delete") in post:
                sql = "delete from Order_GoodsItem where OrderID=%s"
                n = cursor.execute(sql,[order.OrderID]) 
                sql = "delete from BuyerOrder where OrderID = %s"    
                n = cursor.execute(sql,[order.OrderID])  
        sql = "select OrderID,TotalPrice,Orderstate from BuyerOrder where BuyerID = %s and Orderstate = %s"
        cursor.execute(sql,[buyerid,"not payed"])
        or_notpay = []
        for temp in cursor.fetchall():
            or_notpay.append(temp_checkaccount(temp[0],temp[1],temp[2]))
        or_finish = []
        cursor.execute(sql,[buyerid,"finish"])
        for temp in cursor.fetchall():
            or_finish.append(temp_checkaccount(temp[0],temp[1],temp[2]))
        if "submit" in post:
            if "s" in post:
                goodsname = post["s"]
                n = cursor.execute("select GoodsID from Goods where Goodsname = %s",[goodsname]) 
                goodsid = cursor.fetchall()[0][0]
                return HttpResponseRedirect(HOMEPAGE_URL + 'proinfo/' + goodsid +'/') 
        
        if "pay" in post:
            price = post["price"]
            bid = post["orderid"]
            #--Encrypt the URL--#
          
            #TEST = [aim_url,random_key,key_encrypted,random_iv,iv_encrypted,aim_url_encrypted,timestamp,signature]
            #return render_to_response('test.html',locals())
            #return HttpResponseRedirect(VirtualBank_URL + 'cashierdesk/' + aim_url_all)
    cursor.close()
    conn.commit()       
    conn.close()   
    return render_to_response('my-account.html',locals())
    

def editaddress(request):
    error = []
    addr_flag = False
    user_flag = False
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind")  
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    try:
        userid = User.objects.get(username=request.user.username).id
        n = cursor.execute("select BuyerID from Buyer where id = %s",[userid])    
        buyerid = cursor.fetchall()[0][0]   
        user_flag = True
        username = request.user.username
    except:
        user_flag = False
        return HttpResponseRedirect(HOMEPAGE_URL)
    
    n = cursor.execute("select * from BuyerAddrInfo where BuyerID = %s",[buyerid])
    if n != 0:    
        addr_flag = True
        temp = cursor.fetchall()
        buyername = temp[0][3]
        buyerPhone = temp[0][2]
        postcode = temp[0][4]
        buyerAddr = temp[0][1]
        city = temp[0][5]
    else:
        addr_flag = False
    if request.POST:
        post = request.POST
        if not addr_flag:
            name = post["name"]
            phone = post["phone"]
            address =  post["address"]
            city = post["city"]
            postcode = post["postcode"] 
            try:              
                sql = "insert into BuyerAddrInfo(BuyerID,Buyername,BuyerPhone,BuyerAddr,City,Postcode) values(%s,%s,%s,%s,%s,%s)"   
                n = cursor.execute(sql,[buyerid,name,phone,address,city,postcode]) 
            except:
                error.append("此用户地址已存在！")
        else:
            name = post["name"]
            phone = post["phone"]
            address =  post["address"]
            city = post["city"]
            postcode = post["postcode"]               
            sql = "update BuyerAddrInfo set Buyername=%s,BuyerPhone=%s,BuyerAddr=%s,City=%s,Postcode=%s where BuyerID=%s"   
            n = cursor.execute(sql,[name,phone,address,city,postcode,buyerid]) 
            addr_flag = True
            n = cursor.execute("select * from BuyerAddrInfo where BuyerID = %s",[buyerid])
            temp = cursor.fetchall()
            buyername = temp[0][3]
            buyerPhone = temp[0][2]
            postcode = temp[0][4]
            buyerAddr = temp[0][1]
            city = temp[0][5]
    cursor.close()
    conn.commit()    
    conn.close()          
    return render_to_response('edit-address.html',locals())
    
def changepasswd(request):
    error = []
    user_flag = False
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind")  
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    try:
        userid = User.objects.get(username=request.user.username).id
        n = cursor.execute("select BuyerID from Buyer where id = %s",[userid])    
        buyerid = cursor.fetchall()[0][0]   
        user_flag = True
        username = request.user.username
    except:
        user_flag = False
        return HttpResponseRedirect(HOMEPAGE_URL)
    if request.POST:
        post = request.POST
        old_password= post["old_password"]
        new_password= post["new_password"]
        n = cursor.execute("select Password from Buyer where BuyerID = %s",[buyerid])
        passwd = cursor.fetchall()[0][0]
        if old_password == passwd:
            sql = "update Buyer set Password=%s where BuyerID=%s"   
            n = cursor.execute(sql,[new_password,buyerid]) 
            userb = User.objects.get(username=request.user.username)
            userb.set_password(new_password)
            userb.save()
        else:
            error.append("原密码输入错误")
    cursor.close()
    conn.commit()    
    conn.close()   
    return render_to_response('change-password.html',locals())

def addpro(request):
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind") 
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    add_flag = True
    adminname = request.user.username
    if request.POST:
        post = request.POST
        goodsname = post["goodsname"]
        picture = post["picture"]
        price = post["price"]
        stockQua = post["stock"]
        info = post["info"]
        pid = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        caname = post["category"]
        sql = "select KindID from Kind where Kindname = %s"
        cursor.execute(sql,[caname])
        kindid = cursor.fetchall()[0][0]
        sql = "insert into Goods(GoodsID,KindID,Goodsname,Picture,Price,StockQua,Info) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,[pid,kindid,goodsname,picture,price,stockQua,info])
    cursor.close()
    conn.commit()    
    conn.close()      
    return render_to_response("addpro.html",locals())

class temp_editpro:
    Goodsname = None
    Kind = None
    Price = None
    StockQua = None
    Picture = None
    def __init__(self,Goodsname,Kind,Price,StockQua,Picture):
        self.Goodsname = Goodsname
        self.Kind = Kind
        self.Price = Price
        self.StockQua = StockQua
        self.Picture = Picture    


def modpro(request,offset):
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind") 
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    add_flag = False
    adminname = request.user.username
    sql = "select Goodsname,KindID,Price,StockQua,Picture,Info from Goods where Goodsname=%s"
    cursor.execute(sql,[offset])
    temp = cursor.fetchall()
    goodsname = temp[0][0]
    price = temp[0][2]
    stockQua = temp[0][3]
    picture = temp[0][4]
    info = temp[0][5]
    sql = "select Kindname from Kind where KindID = %s"
    cursor.execute(sql,[temp[0][1]])
    kindname = cursor.fetchall()[0][0]
    if request.POST:
        post = request.POST
        caname = post["category"]
        sql = "select KindID from Kind where Kindname = %s"
        cursor.execute(sql,[caname])
        kindid = cursor.fetchall()[0][0]
        goodsname = post["goodsname"]
        price = post["price"]
        picture = post["picture"]
        stockQua = post["stock"]
        info = post["info"]
        sql = "update Goods set KindID =%s,Goodsname=%s,Picture=%s,Price=%s,StockQua=%s,Info=%s where Goodsname=%s"
        cursor.execute(sql,[kindid,goodsname,picture,price,stockQua,info,offset])
    cursor.close()
    conn.commit()    
    conn.close()       
    return render_to_response("addpro.html",locals())

class temp_cart:
    ItemID = None
    Goodsname = None
    GoodsID = None
    Price = None
    Quantity = None
    Picture = None
    def __init__(self,ItemID,Goodsname,GoodsID,Price,Quantity,Picture):
        self.ItemID = ItemID
        self.Goodsname = Goodsname
        self.GoodsID = GoodsID
        self.Price = Price
        self.Quantity = Quantity
        self.Picture = Picture    
    

def checkcart(request):
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind") 
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    error = []
    user_flag = False
    try:
        userid = User.objects.get(username=request.user.username).id
        n = cursor.execute("select BuyerID from Buyer where id = %s",[userid])    
        buyerid = cursor.fetchall()[0][0]   
        user_flag = True
        username = request.user.username
    except:
        user_flag = False
        return HttpResponseRedirect(HOMEPAGE_URL)
    item = []
    sql = "select GoodsItem.ItemID,Goodsname,GoodsID,AllPrice,Quantity,Picture from GoodsItem,Cart_GoodsItem where GoodsItem.ItemID = Cart_GoodsItem.ItemID and BuyerID = %s "
    cursor.execute(sql,[buyerid])
    for temp in cursor.fetchall():
        item.append(temp_cart(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5]))
    if request.POST:
        post = request.POST
        for it in item:
            if(it.ItemID + "_delete") in post:
                sql = "delete from Cart_GoodsItem where ItemID =%s"
                cursor.execute(sql,[it.ItemID])
                sql = "delete from GoodsItem where ItemID =%s"
                cursor.execute(sql,[it.ItemID])
                
        item = []
        sql = "select GoodsItem.ItemID,Goodsname,GoodsID,AllPrice,Quantity,Picture from GoodsItem,Cart_GoodsItem where Cart_GoodsItem.ItemID =GoodsItem.ItemID and BuyerID = %s "
        cursor.execute(sql,[buyerid])
        for temp in cursor.fetchall():
            item.append(temp_cart(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5]))
        if "submit" in post:
            if "s" in post:
                goodsname = post["s"]
                n = cursor.execute("select GoodsID from Goods where Goodsname = %s",[goodsname]) 
                goodsid = cursor.fetchall()[0][0]
                return HttpResponseRedirect(HOMEPAGE_URL + 'proinfo/' + goodsid +'/')
    cursor.close()
    conn.commit()    
    conn.close()   
    return render_to_response('cart.html',locals())
    
class temp_confirmorder:
    GoodsID = None
    Picture = None
    Goodsname = None
    Quantity = None
    Price = None
    def __init__(self,GoodsID,Picture,Goodsname,Quantity,Price):
        self.GoodsID = GoodsID
        self.Picture = Picture
        self.Goodsname = Goodsname
        self.Quantity = Quantity
        self.Price = Price    

def confirmorder(request):
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind") 
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    user_flag = False
    try:
        userid = User.objects.get(username=request.user.username).id
        user_flag = True
        username = request.user.username
    except:
        user_flag = False
        return HttpResponseRedirect(HOMEPAGE_URL)
    sql = "select BuyerID from Buyer where id = %s"
    cursor.execute(sql,[userid])
    buyerid = cursor.fetchall()[0][0]
    n = cursor.execute("select * from BuyerAddrInfo where BuyerID = %s",[buyerid])
    if n == 0:
        return HttpResponseRedirect(HOMEPAGE_URL + 'editaddress')
    else:
        temp = cursor.fetchall()
        city = temp[0][5]
        buyerAddr = temp[0][1]
        buyername = temp[0][3]
        buyerPhone = temp[0][2]
    if request.POST:
        post = request.POST
        if "flag_fromcart" in post:
            item = []
            all_ItemID = post["all_ItemID"]
            item = post["all_ItemID"].split("$")
            item1 = []
            for it in item:
                if it != '':
                    item = []
                    sql = "select GoodsID,Picture,Goodsname,Quantity,AllPrice from GoodsItem where ItemID = %s "
                    cursor.execute(sql,[it])
                    for temp in cursor.fetchall():
                        item1.append(temp_confirmorder(temp[0],temp[1],temp[2],temp[3],temp[4]))
            price = post["all_Price"]
        if "submit" in post:
            price= post["getprice"]
            item1= post["getitem"]
            item = []
            item = item1.split("$")
            bid = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + str(random.randrange(1000,9999))
            time1 = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            sql = "insert into BuyerOrder(OrderID,BuyerID,Time,TotalPrice,Orderstate) values(%s,%s,%s,%s,%s)"
            cursor.execute(sql,[bid,buyerid,time1,price,"not payed"])
            for it in item:
                if it != '':
                    sql = "insert into Order_GoodsItem(OrderID,ItemID) values(%s,%s)"
                    cursor.execute(sql,[bid,it])
                    sql = "delete from Cart_GoodsItem where ItemID=%s"
                    cursor.execute(sql,[it])
            cursor.close()
            conn.commit()    
            conn.close()   
            return HttpResponseRedirect(HOMEPAGE_URL)
    cursor.close()
    conn.commit()    
    conn.close()   
    return render_to_response("confirmorder.html",locals())


      

def editpro(request):
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind") 
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    sql = "select GoodsID from Goods"
    cursor.execute(sql)
    pro = []
    for per in cursor.fetchall():
        pro.append(per[0])
    
    sql = "select Goodsname,KindID,Price,StockQua,Picture from Goods"
    cursor.execute(sql)
    pro = []
    for temp in cursor.fetchall():
        sql = "select Kindname from Kind where KindID = %s"
        cursor.execute(sql,[temp[1]])
        kindname = cursor.fetchall()[0][0]
        pro.append(temp_editpro(temp[0],kindname,temp[2],temp[3],temp[4]))
    adminname = request.user.username
    if request.POST:
        post = request.POST
        for pr in pro:
            if (pr.Goodsname +"_delete") in post:
                sql = "delete from Goods where Goodsname = %s"
                cursor.execute(sql,[pr.Goodsname])
        sql = "select Goodsname,KindID,Price,StockQua,Picture from Goods"
        cursor.execute(sql)
        pro = []
        for temp in cursor.fetchall():
            sql = "select Kindname from Kind where KindID = %s"
            cursor.execute(sql,[temp[1]])
            kindname = cursor.fetchall()[0][0]
            pro.append(temp_editpro(temp[0],kindname,temp[2],temp[3],temp[4]))
    cursor.close()
    conn.commit()    
    conn.close()   
    return render_to_response("productinfo.html",locals())
class temp_shop:
    GoodsID = None
    Picture = None
    Goodsname = None
    Price = None
    def __init__(self,GoodsID,Picture,Goodsname,Price):
        self.GoodsID = GoodsID
        self.Picture = Picture
        self.Goodsname = Goodsname
        self.Price = Price    

def shop(request):
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind") 
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    user_flag = False
    try:
        userid = User.objects.get(username=request.user.username).id
        user_flag = True
        username = request.user.username
    except:
        user_flag = False
    sql = "select * from Goodsshort"
    cursor.execute(sql)
    pro = []
    for temp in cursor.fetchall():
        pro.append(temp_shop(temp[0],temp[1],temp[2],temp[3]))
    cursor.close()   
    conn.close()   
    return render_to_response('shop.html',locals())

def proinfo(request,offset):
    user_flag = False
    try:
        userid = User.objects.get(username=request.user.username).id
        user_flag = True
        username = request.user.username
    except:
        user_flag = False
        return HttpResponseRedirect(HOMEPAGE_URL)
    
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind") 
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    cursor.execute("select BuyerID from Buyer where id = %s",[userid])
    buyerid = cursor.fetchall()[0][0]
    sql = "select * from Goods where GoodsID = %s"
    cursor.execute(sql,[offset])
    temp = cursor.fetchall()
    goodsID = offset
    goodsname = temp[0][2]
    picture = temp[0][3]
    price = temp[0][4]
    stockQua = temp[0][5]
    info = temp[0][6]
    cursor.execute("select KindID from Goods where GoodsID = %s",[goodsID])
    kindid = cursor.fetchall()[0][0]
    sql = "select Kindname from Kind where KindID = (select KindID from Goods where GoodsID = %s)"
    cursor.execute(sql,[goodsID])
    goodskind = cursor.fetchall()[0][0]
#    good = Goods.objects.get(GoodsID = offset)
#    gooda = Goods.objects.filter(Cate = good.Cate)
#    good_list = list(gooda)
#    good_list.remove(good)
#   
    good_list = []     
    sql = "select * from Goodsshort where GoodsID <> %s and KindID = %s "
    cursor.execute(sql,[goodsID,kindid])
    for temp in cursor.fetchall():
        good_list.append(temp_shop(temp[0],temp[1],temp[2],temp[3]))
    if request.POST:
        post =request.POST
        try:
            qua = post["quantity"]
        except:
            qua = "1"
        if (goodsID+"_add") in post:
            total = float(price) * int(qua)
            bid = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + str(random.randrange(1000,9999))
            sql = "insert into GoodsItem(ItemID,GoodsID,Goodsname,AllPrice,Picture,Quantity) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,[bid,goodsID,goodsname,total,picture,qua])
            sql = "insert into Cart_GoodsItem(BuyerID,ItemID) values(%s,%s)"
            cursor.execute(sql,[buyerid,bid])
            cursor.close()
            conn.commit()    
            conn.close()  
            return HttpResponseRedirect(HOMEPAGE_URL + 'addsuccess/' + goodsID +'/') 
         
        
    return render_to_response('product_single.html',locals())

class temp_viewdetail:
    GoodsID = None
    Picture = None
    Goodsname = None
    Quantity = None
    Price = None
    def __init__(self,GoodsID,Picture,Goodsname,Quantity,Price):
        self.GoodsID = GoodsID
        self.Picture = Picture
        self.Goodsname = Goodsname
        self.Quantity = Quantity
        self.Price = Price    
def viewdetail(request,offset):
    user_flag = False
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind")  
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    #TEST = offset
    #return render_to_response('test.html',locals())
    #enorderid = offset
    #orderid = decryptedString(rsa_key,enorderid)
    orderid = offset
    sql = "select Time from BuyerOrder where OrderID = %s"
    cursor.execute(sql,[orderid])
    ordertime = cursor.fetchall()[0][0]
    try:
        userid = User.objects.get(username=request.user.username).id
        user_flag = True
        username = request.user.username
    except:
        user_flag = False
        return HttpResponseRedirect(HOMEPAGE_URL)
    sql = "select GoodsID,Picture,Goodsname,Quantity,AllPrice from GoodsItem where ItemID = (select ItemID from Order_GoodsItem where OrderID=%s)"
    cursor.execute(sql,[offset])
    item = []
    for temp in cursor.fetchall():
        item.append(temp_viewdetail(temp[0],temp[1],temp[2],temp[3],temp[4]))
    cursor.close()   
    conn.close()
    return render_to_response('viewdetail.html',locals())

def addsuccess(request,offset):
    user_flag = False
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind")  
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    try:
        userid = User.objects.get(username=request.user.username).id
        user_flag = True
        username = request.user.username
    except:
        user_flag = False
        return HttpResponseRedirect(HOMEPAGE_URL)
    goodsID = offset
    sql = "select * from Goodsshort where GoodsID = %s"
    cursor.execute(sql,[goodsID])
    temp = cursor.fetchall()
    goodsname = temp[0][2]
    picture = temp[0][1]
    cursor.close()   
    conn.close()
    return render_to_response("addsuccess.html",locals())
    
class temp_statistics:
    BuyerID = None
    Count = None
    def __init__(self,BuyerID,Count):
        self.BuyerID = BuyerID
        self.Count = Count

def statistics(request):
    user_flag = False
    conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    n = cursor.execute("select * from Allkind")  
    catalist = []
    kind = cursor.fetchall()
    for cata in kind:
        catalist.append(cata[0])
    try:
        userid = User.objects.get(username=request.user.username).id
        user_flag = True
        adminname = request.user.username
    except:
        user_flag = False
    sql = "select BuyerID,count(OrderID) from BuyerOrder group by BuyerID having count(OrderID) > 3 order by count(OrderID) DESC"
    cursor.execute(sql)
    pro = []
    for temp in cursor.fetchall():
        pro.append(temp_statistics(temp[0],temp[1]))
    cursor.close()   
    conn.close()
    return render_to_response("statics.html",locals())