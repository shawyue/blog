# _*_ coding:utf-8 _*_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import uuid
from random import randint
import datetime
import re
from logbook import Logger


from . import mysql_client, login_manager, redis_client

log = Logger("MODELS")

class GenerateArticleID(object):

    def __new__(self):
        
        if not hasattr(self, 'instance'):
            self.instance = super(GenerateArticleID, self).__new__(self)
        return self.instance

    def __init__(self):
        self.cache()

    @staticmethod
    def byte_to_int(data):
        if isinstance(data, bytes):
            return int(data)
        else:
            return False

    def get(self):
        unique_id = redis_client.get("unique_id")
        if unique_id == b'None':
            unique_id = 1000000
            redis_client.set("unique_id", unique_id)
            log.debug(redis_client.get("unique_id"))
            return unique_id
        else:
            unique_id = self.byte_to_int(unique_id)
            new_unique_id = unique_id + 1
            redis_client.set("unique_id", new_unique_id)
            return new_unique_id
    
    def cache(self):
       return  redis_client.set("unique_id", self.get_max_id())

    def get_max_id(self):
        self.unique_id = mysql_client.fetch_one("SELECT MAX(UNIQUEID) FROM ARTICLES")[0]
        return self.unique_id


class Article(object):

    def __init__(self, unique_id=None):
        self.unique_id = str(unique_id)
        self.generateArticleID = GenerateArticleID()
        self.user_id = current_user.get_id()

    def save_about(self, about):
        #now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if about != None and about != "":
            mysql_client.execute("UPDATE OPTIONS SET ABOUT = %s WHERE USERID = %s", (about, self.user_id))
            mysql_client.commit()
            return True

    def get_about(self):
        about_info = mysql_client.fetch_one("SELECT ABOUT FROM OPTIONS WHERE USERID = %s", (self.user_id))
        if about_info != None:
            return about_info[0]
        else:
            return None

    def save_tips(self, tips):
        #now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if tips != None and tips != "":
            mysql_client.execute("UPDATE OPTIONS SET TIPS = %s WHERE USERID = %s", (tips, self.user_id))
            mysql_client.commit()
            return True

    def get_tips(self):
        tips_info = mysql_client.fetch_one("SELECT TIPS FROM OPTIONS WHERE USERID = %s", (self.user_id))
        if tips_info != None:
            return tips_info[0]
        else:
            return None

    def get_all_abstract(self, article_type=None):
        if article_type == None:
            abstract = mysql_client.fetch_all("SELECT ABSTRACT FROM ARTICLES WHERE USERID = %s", (self.user_id))
            return abstract
        else:
            abstract = mysql_client.fetch_all("SELECT ABSTRACT FROM ARTICLES WHERE USERID = %s AND TYPEID=%s", (self.user_id, article_type))
            return abstract

    def get_article(self):
        article = mysql_client.fetch_one("SELECT ARTICLE FROM ARTICLES WHERE UNIQUEID = %s", (self.unique_id))
        return article


    def save_article(self, article_text, article_type):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.unique_id == 'None':
            self.unique_id = str(self.generateArticleID.get())
            mysql_client.execute("INSERT INTO ARTICLES (ID, USERID, ARTICLE, TYPEID, CREATETIME, UNIQUEID) VALUES(0, %s, %s, %s, %s, %s)", (self.user_id, article_text, article_type, now_time, self.unique_id))
            mysql_client.commit()
            data = self.get_abstract_data(article_text)
            abstract = self.generate_abstract(data)
            log.debug(self.save_abstract(abstract))
            mysql_client.commit()
            return self.unique_id
        else:
            mysql_client.execute("UPDATE ARTICLES SET ARTICLE = %s, MODIFYTIME = %s WHERE UNIQUEID = %s",(article_text, now_time, self.unique_id))
            mysql_client.commit()
            return self.unique_id
    
    def save_abstract(self, abstract_text):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mysql_client.execute("UPDATE ARTICLES SET ABSTRACT = %s, MODIFYTIME = %s WHERE UNIQUEID = %s",(abstract_text, now_time, self.unique_id))
        mysql_client.commit()
        return self.unique_id
    
    @staticmethod
    def get_abstract_data(article):
        paragraph_len = 230
        title_pattern = re.compile("<[^<>]*h[^<>]*>([^<>]*)<[^<>]*/h[^<>]*>")
        title_match = title_pattern.search(article)
        if not title_match is None:
            title = title_match[1].strip()
        else:
            title = ""
        video_pattern = re.compile("<[^<>]*video[^<>]*>([^<>]*)<[^<>]*/video[^<>]*>")
        video_match = video_pattern.search(article)
        if not video_match is None:
            video = video_match[0].strip()
        else:
            video = ""  
        img_pattern = re.compile("<[^<>]*img[^<>]*alt[^<>]*/[^<>]*>")
        img_match = img_pattern.search(article)
        if not img_match is None:
            img = img_match[0].strip()
        else:
            img = ""  
        article = article.replace("<[^<>]*br[^<>]*/[^<>]*>", " ")
        paragraph_pattern = re.compile("<[^<>]*p[^<>]*>([^<>]*)<[^<>]*/p[^<>]*>")
        paragraph_match = paragraph_pattern.findall(article)
        paragraph = ""
        if not paragraph_match is None:
            
            for p in paragraph_match:
                if p.strip()!="":
                    paragraph = paragraph + p.strip()
                    if len(paragraph) < paragraph_len-60 and len(paragraph) > 0:
                        paragraph = paragraph + "<br/>"
                        
                    else:
                        break
            paragraph = paragraph[0:400]
        return {"title": title, "video": video, "img": img, "paragraph": paragraph}

    def generate_abstract(self, data):
        url = "/article/detail?id=" + self.unique_id
        if data["video"] != "":
            return '''
            <h3>%s</h3><p><span ><a href="%s" class="itermpic">%s</a>%s</span></p>
            <a href="%s" target="_blank" class="readmore">阅读全文&gt;&gt;</a>
            ''' % (data["title"], url, data["video"], data["paragraph"], url )
        elif data["img"] != "":
            return '''
            <h3>%s</h3><p><span ><a href="%s" class="itermpic">%s</a>%s</span></p>
            <a href="%s" target="_blank" class="readmore">阅读全文&gt;&gt;</a>
            ''' % (data["title"], url, data["img"], data["paragraph"], url)
        else:
            return '''
            <h3>%s</h3><p><span >%s</span></p>
            <a href="%s" target="_blank" class="readmore">阅读全文&gt;&gt;</a>
            ''' % (data["title"], data["paragraph"], url)

    def get_abstract(self):
        abstract = mysql_client.fetch_one("SELECT ABSTRACT FROM ARTICLES WHERE UNIQUEID = %s", (self.unique_id))
        return abstract

class User(UserMixin):

    def __init__(self, user_id):
        
        #self.username = username
        self.id = user_id
        self.password_hash = self.get_password_hash()


    @property
    def password(self):
        raise AttributeError("password is not readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        mysql_client.execute("UPDATE USERS SET PASSWD = %s WHERE ID = %s",(self.password_hash, self.id))
        mysql_client.commit()

    def verify_password(self, password):
        res = check_password_hash(self.password_hash, password)
        log.debug(res)
        return res
    def get_password_hash(self):
        user_info = mysql_client.fetch_one("SELECT PASSWD FROM USERS WHERE ID = %s", (self.id))
        if user_info is not  None:
            return user_info[0]
    
    @staticmethod
    def generate_token(json_data, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(json_data)
    
    @staticmethod
    def parse_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        return data

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        if user_id is not None:
            return User(user_id)
        else:
            return None

    


class AnonymousUser(AnonymousUserMixin):

    def __init__(self):
        pass
    
    def get_id(self):
        return uuid.uuid4()


class RegisterUser(object):

    def __init__(self):
        pass
    
    @staticmethod
    def get_id(email):
        if email is not None:
            id_info = mysql_client.fetch_one("SELECT ID FROM USERS WHERE email = %s", (email))
            log.debug(id_info)
            if id_info is not None:
                return id_info[0]
            else:
                return None

    @staticmethod   
    def verify_username(username):
        
        id_info = mysql_client.fetch_one("SELECT ID FROM USERS WHERE nickname = %s", (username))
        log.debug(id_info)
        if id_info is None:
            return True
        else:
            return False

    @staticmethod
    def register( user_info):
        tips = "热爱生活的都是好孩子"
        about = ""
        username = user_info.get("username", None)
        password = user_info.get("password", None)
        email = user_info.get("email", None)
        if (username != None and password != None and email != None):
            password_hash = generate_password_hash(password)
            mysql_client.execute("INSERT INTO USERS (id, nickname, passwd, roleid, email) VALUES(0, %s, %s, 2, %s)", (username, password_hash, email))
            mysql_client.commit()
            user_id = RegisterUser.get_id(email)
            mysql_client.execute("INSERT INTO OPTIONS (id, USERID, tips, about) VALUES(0, %s, %s, %s)", (user_id, tips, about))
            mysql_client.commit()
            return True
        return False

    @staticmethod
    def verify_email(email):

        log.debug(email)
        id_info = mysql_client.fetch_one("SELECT ID FROM USERS WHERE email = %s", (email))
        log.debug(id_info)
        if id_info is None:
            return True
        else:
            return False

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class Captcha(object):
    def __init__(self):
        pass

    def save_captcha(self, email, captcha):
        return redis_client.set(email, captcha, 600)

    def get_captcha(self, email):
        return redis_client.get(email)

    def generate_captcha(self):
        b = 0
        captcha = ""
        while b < 6:
            captcha = captcha + str(randint(0, 9))
            b = b + 1
        return captcha

    def verify_captcha(self, email, captcha):
        redis_captcha = self.get_captcha(email).decode("utf-8")
        return redis_captcha==captcha
