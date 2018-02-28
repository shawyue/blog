-- 数据库初始化语句
create database myblog; --创建数据库

create user 'username'@'host' identified by 'password'; --创建mysql用户,host设为%可在任意主机登录
GRANT all privileges ON blog.* TO 'username'@'host'; --赋予用户权限 

create table ROLE(
    id int unsigned auto_increment,
    name varchar(50) unique not null,
    DefaultValue tinyint(1) default 0,
    premissions int(8) default 0,
    primary key(id)
);
--插入基础数据
insert into ROLE values(1,'ADMINSTER', 1, 0xff); --admin
insert into ROLE values(2,'USER', 1, 0x07);      --用户

-- 常见文章类型表
create table ARTICLE_TYPE (
    id int unsigned auto_increment,
    type varchar(40),
    primary key(id)
);
--初始化文章类型数据
insert into ARTICLE_TYPE  values(1,'blog article');
insert into ARTICLE_TYPE  values(2,'life essay');


-- 创建用户表
create table USERS (
    id int unsigned auto_increment,
    nickname varchar(50) not null ,
    passwd char(128) not null,
    roleID int unsigned not null, 
    email char(128) not null,
    phone char(20),
    IDCardNo char(18),
    firstName char(30),
    lastName char(30),
    signUpIP char(15),
    signUpDate datetime,
    unique(nickname),
    primary key(id)
)

--创建设置表
create table OPTIONS(
    id int unsigned auto_increment,
    userID int unsigned not null,
    tips char(255),
    about text,
    unique(userID),
    primary key(id)
);

--创建文章表
create table ARTICLES(
    id int unsigned auto_increment,
    userID int unsigned not null,
    article mediumtext,
    typeID int unsigned,
    abstract varchar(5000),
    UniqueID int unique,
    createTime datetime,
    modifyTime datetime,
    primary key(id)
);
