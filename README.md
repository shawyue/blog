# BLOG

这个仓库为使用flasky开发的一个简单blog网站，用于学习及研究flasky特性，现阶段有的登录，注册，文章编写，保存，展示，等功能。

## 使用

注意：使用的Python为3.6.4， mysql为5.7.21

1,克隆仓库

        git clone https://github.com/shawyue/blog.git


2,安装redis, mysql

        sudo apt-get install redis-server
        sudo apt-get install mysql-server
        sudo apt-get install mysql-client

3,使用database.sql中的命令初始化数据库

4,安装python库

        pip install -r requirements.txt
 
5,设置配置

        设置config.py中的配置，配置mysql, redis, 邮箱等
 
6,运行

        进入目录，Python3 manage.py runserver
