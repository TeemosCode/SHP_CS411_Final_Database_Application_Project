# -*- coding: utf-8 -*-
"""
Created on Wed May 11 23:43:02 2016

@author: apple
"""
import MySQLdb

def mysql_init():
    #连接    
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="SellWeb_mysql",charset="utf8")  
    cursor = conn.cursor()    
    
    ##删除表
    #sql = "drop table if exists user"
    #cursor.execute(sql)
    
    ##创建
    #sql = "create table if not exists user(name varchar(128) primary key, created int(10))"
    #cursor.execute(sql)
    
    #创建
#    sql = "create table if not exists User(username varchar(100) not null, password varchar(100) not null,primary key(username))"
#    cursor.execute(sql)
    
    sql = "create table if not exists Buyer(BuyerID varchar(100) not null, Username varchar(100) not null,Password varchar(128) not null,id int(11) not null,Phone varchar(11),Email varchar(100) not null,primary key(BuyerID),foreign key(id) references auth_user(id))"
    cursor.execute(sql)
    
    sql = "create table if not exists BuyerAddrInfo(BuyerID varchar(100) not null,BuyerAddr varchar(100) not null, BuyerPhone varchar(11) not null,Buyername varchar(100) not null,Postcode varchar(100),City varchar(10),primary key(Buyername),foreign key(BuyerID) references Buyer(BuyerID))"
    cursor.execute(sql)
    
    sql = "create table if not exists Admin(Adminname varchar(100) not null, AdminPasswd varchar(128) not null,id int(11) not null,primary key(Adminname),foreign key(id) references auth_user(id))"
    cursor.execute(sql)
    
    sql = "create table if not exists Kind(KindID varchar(100) not null, Kindname varchar(100) not null,primary key(KindID))"
    cursor.execute(sql)
    
    sql = "create table if not exists Goods(GoodsID varchar(100) not null,KindID varchar(100) not null, Goodsname varchar(100) not null,Picture varchar(100) not null,Price varchar(20) not null,StockQua varchar(20) not null,Info varchar(1000),primary key(GoodsID),foreign key(KindID) references Kind(KindID))"
    cursor.execute(sql)
    
    #***************
    sql = "create table if not exists GoodsItem(ItemID varchar(100) not null, GoodsID varchar(100) not null,Goodsname varchar(100) not null,AllPrice varchar(20) not null,Picture varchar(100) not null,Quantity varchar(5) not null,primary key(ItemID),foreign key(GoodsID) references Goods(GoodsID))"
    cursor.execute(sql)    
    
    sql = "create table if not exists Cart_GoodsItem(BuyerID varchar(100) not null, ItemID varchar(100) not null,primary key(BuyerID,ItemID),foreign key(ItemID) references GoodsItem(ItemID),foreign key(BuyerID) references Buyer(BuyerID))"
    cursor.execute(sql)
    
    sql = "create table if not exists Order_GoodsItem(OrderID varchar(100) not null, ItemID varchar(100) not null,primary key(OrderID,ItemID),foreign key(ItemID) references GoodsItem(ItemID),foreign key(OrderID) references BuyerOrder(OrderID))"
    cursor.execute(sql)
    
    sql = "create table if not exists BuyerOrder(OrderID varchar(100) not null, BuyerID varchar(100) not null,Time varchar(50) not null,TotalPrice varchar(11),Orderstate varchar(11) not null,primary key(OrderID),foreign key(BuyerID) references Buyer(BuyerID))"
    cursor.execute(sql)
    
    sql = "create view Allkind as select Kindname from Kind"
    cursor.execute(sql)
    
    sql = "create view Goodsshort as select GoodsID,Picture,Goodsname,Price,KindID from Goods"
    cursor.execute(sql) 
    
    sql = "create index BuyerID_Index on BuyerOrder(BuyerID ASC)"
    cursor.execute(sql)
    ##写入    
    #sql = "insert into user(name,created) values(%s,%s)"   
    #param = ("aaa",int(time.time()))    
    #n = cursor.execute(sql,param)    
    #print 'insert',n    
    #   
    ##写入多行    
    #sql = "insert into user(name,created) values(%s,%s)"   SellWebDB Sellapp_goods
    #param = (("bbb",int(time.time())), ("ccc",33), ("ddd",44) )
    #n = cursor.executemany(sql,param)    
    #print 'insertmany',n    
    #
    ##更新    
    #sql = "update user set name=%s where name='aaa'"   
    #param = ("zzz")    
    #n = cursor.execute(sql,param)    
    #print 'update',n    
    #   
    ##查询    
    #n = cursor.execute("select * from user")    
    #for row in cursor.fetchall():    
    #    print row
    #    for r in row:    
    #        print r    
    #   
    ##删除    
    #sql = "delete from user where name=%s"   
    #param =("bbb")    
    #n = cursor.execute(sql,param)    
    #print 'delete',n    
    #
    ##查询    
    #n = cursor.execute("select * from user")    
    #print cursor.fetchall()    
    #
    cursor.close()    
       
    #提交    
    conn.commit()
    #关闭    
    conn.close()   