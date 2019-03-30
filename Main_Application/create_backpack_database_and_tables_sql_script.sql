CREATE DATABASE backpack;
USE backpack;

-- DROP TABLE Tag;
create table BUser(
userid int not null AUTO_INCREMENT,
primary key (userid),
open_match int,
nickname varchar(50),
info varchar(500),
profile_pic varchar(200),
);

create table BlogPost(
postid int not null AUTO_INCREMENT,
primary key (postid),
title varchar(100),
content varchar(10000),
create_time datetime,
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
tag_name varchar(50),
tag_type varchar(50)
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

create table Travelinfo(
travelinfo_id int not null AUTO_INCREMENT,
primary key (travelinfo_id),
activity varchar(200),
budgetMax int,
budgetMin int,
destination varchar(100),
startTime date,
endTime date,
userid int,
foreign key (userid) references BUser(userid)
on delete cascade
);

create table Comment(
commentid int not null AUTO_INCREMENT,
primary key (commentid),
comment_time datetime,
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
