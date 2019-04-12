-- DROP DATABASE backpack;
CREATE DATABASE backpack;
USE backpack;


create table BUser(
userid int not null AUTO_INCREMENT,
primary key (userid),
open_match int,
username varchar(50) UNIQUE,
profile_pic varchar(200),
firstname varchar(50) DEFAULT '',
lastname varchar(50) DEFAULT '',
email varchar(50),
info varchar(10000)
);

create table BlogPost(
postid int not null AUTO_INCREMENT,
primary key (postid),
title varchar(100),
content varchar(10000),
create_time datetime not null DEFAULT CURRENT_TIMESTAMP,
author int,

foreign key (author) references BUser(userid)
on delete cascade
);

create table BlogPhoto(
photoid int not null AUTO_INCREMENT,
primary key (photoid),
photo_url varchar(100),
postid int not null,
foreign key (postid) references BlogPost(postid)
on delete cascade
);

create table Tag(
tagid int not null AUTO_INCREMENT,
primary key (tagid),
tag_name varchar(50) NOT NULL,
tag_type varchar(50) NOT NULL,
UNIQUE(tag_name, tag_type)
);

create table BlogTag(
postid int not null,
tagid int not null,
primary key (postid, tagid),
foreign key (postid) references BlogPost(postid)
on delete cascade,
foreign key (tagid) references Tag(tagid)
on delete cascade
);

create table UserTag(
userid int not null,
tagid int not null,
primary key (userid, tagid),
foreign key (userid) references BUser(userid)
on delete cascade,
foreign key (tagid) references Tag(tagid)
on delete cascade
);

create table Travelinfo (
travelinfo_id int not null AUTO_INCREMENT,
primary key (travelinfo_id),
activity varchar(200) DEFAULT '',
budgetMax int DEFAULT 0,
budgetMin int DEFAULT 0,
destination varchar(100) DEFAULT '',
startTime date DEFAULT NULL,
endTime date DEFAULT NULL,
userid int,
foreign key (userid) references BUser(userid)
on delete cascade
);

create table Comment (
commentid int not null AUTO_INCREMENT,
primary key (commentid),
comment_time datetime DEFAULT CURRENT_TIMESTAMP,
content varchar(5000),
postid int,
userid int not null,
parentid int,
foreign key (postid) references BlogPost(postid)
on delete cascade,
foreign key (parentid) references Comment(commentid)
on delete cascade,
foreign key (userid) references BUser(userid)
on delete cascade
);

create table LikePost(
userid int not null,
postid int not null,
primary key (userid, postid),
foreign key (userid) references BUser(userid)
on delete cascade,
foreign key (postid) references BlogPost(postid)
on delete cascade
);

