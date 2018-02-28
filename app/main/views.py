# _*_ coding:utf-8 _*_

import os
import re
import base64
import datetime
import random
from flask import render_template, request, send_from_directory, jsonify
from flask_login import login_required
from logbook import Logger

from . import main
from app import ueditor, mysql_client
from app.models import Article

log = Logger("MAIN.VIEWS")

def save_article(article, article_type):
    article_obj = Article()
    if article_type == "life":
        unique_id = article_obj.save_article(article, '2')
    elif article_type == "about":
        article_obj.save_about(article)
        return "about article"
    else:
        unique_id = article_obj.save_article(article, '1')
    log.debug(unique_id)
    return unique_id

def genrate_abstract_content(fetch_abstract):
    abstract_content = ""
    log.debug(fetch_abstract)
    index = 1
    for rows in fetch_abstract:
        if index % 2 == 1:
            abstract_content = abstract_content + """<div class="iterm" data-scroll-reveal="enter left over 1s" >""" \
            + rows[0] + """</div>"""
            index = index + 1
        elif index % 2 == 0:
            abstract_content = abstract_content + """<div class="iterm" data-scroll-reveal="enter right over 1s" >""" \
            + rows[0] + """</div>"""
            index = index + 1
    return abstract_content

@main.route("/article/about")
@login_required
def get_about():
    article_obj = Article()
    about = article_obj.get_about()
    return jsonify({"result": 1, "about": about})

@main.route("/article/abstract")
@login_required
def get_abstract():
    action_dict = request.args
    article_obj = Article()
    log.debug(action_dict)
    if action_dict:
        action = action_dict.get("action", None)
        log.debug(action)
        if action == "all":
            fetch_abstract = article_obj.get_all_abstract()
        elif action == "blog":
            fetch_abstract = article_obj.get_all_abstract(1)
        elif action == "life":
            fetch_abstract = article_obj.get_all_abstract(2)
        
        abstract_content = genrate_abstract_content(fetch_abstract)
        return jsonify({"result":1, "abstract": abstract_content})
    else:
        return jsonify({"result":0, "abstract": ""})

@main.route("/article/detail/<unique_id>")
@login_required
def load_article(unique_id):
    unique_id = unique_id
    article_obj = Article(unique_id)
    article = article_obj.get_article()
    log.debug(article)  
    return jsonify({"result":1, "article":article[0]})

@main.route("/article/detail")
@login_required
def detial():

    return render_template("detail.html")

@main.route("/upload/article", methods=["POST"])
@login_required
def upload_article():
    log.debug(request.form)
    action = request.form.get("action", None).strip()
    article = request.form.get("editorContent", None).strip()
    log.debug(article)   
    if not article is None:
        save_article(article, action)
        log.debug(article)
        #print(article_obj.save(article))
        return jsonify({"result":1})
    else:
        return jsonify({"result":0})
def get_file_name(upload_original_ext):
    param = {
        "year":datetime.datetime.now().strftime("%Y"),
        "month":datetime.datetime.now().strftime("%m"),
        "day":datetime.datetime.now().strftime("%d"),
        "date": datetime.datetime.now().strftime("%Y%m%d"),
        "time":datetime.datetime.now().strftime("%H%M%S"),
        "datetime":datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "rnd":random.randrange(100,999)
    }
    return  str(param["datetime"]) + str(param["rnd"]) + upload_original_ext

#保存上传的文件
def save_upload_file(PostFile,FilePath):
    try:
        f = open(FilePath, 'wb')
        f.write(PostFile)
    except Exception as E:
        f.close()
        return "写入文件错误:"+ str(E)
    f.close()
    return "SUCCESS"

@main.route('/upload/<path>/<filename>')
def get_uploaded_file(path, filename):
    log.debug(filename)
    return send_from_directory("/upload/" + path,filename)

@main.route("/ueditor/upload/", methods=["GET","POST"])
@login_required
def ueditor_upload():
    action = request.args.get('action')
    ueditor_config = ueditor.get_config()
    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = ueditor_config
        return jsonify(result)

    all_upload_field_name={
        "uploadfile":"fileFieldName","uploadimage":"imageFieldName",
        "uploadscrawl":"scrawlFieldName","catchimage":"catcherFieldName",
        "uploadvideo":"videoFieldName",
    }
    upload_field_name = ueditor_config.get(all_upload_field_name.get(action, None), "upfile")


    if action=="uploadscrawl":
        upload_file_name="scrawl.png"
        #upload_file_size=0
    else:
        #取得上传的文件
        upfile = request.files[upload_field_name]
        upload_file_name = upfile.filename
        log.debug(upload_file_name)

    upload_original_name,upload_original_ext=os.path.splitext(upload_file_name)
    log.debug(upload_original_name)
    #文件类型检验
    upload_allow_type={
        "uploadfile":"fileAllowFiles",
        "uploadimage":"imageAllowFiles",
        "uploadvideo":"videoAllowFiles"
    }

    if action in upload_allow_type.keys():
        allow_type= ueditor_config.get(upload_allow_type.get(action, None), [])
        if not upload_original_ext.lower()  in allow_type:
            state=u"服务器不允许上传%s类型的文件。" % upload_original_ext

    upload_path_format={
        "uploadfile":"filePathFormat",
        "uploadimage":"imagePathFormat",
        "uploadscrawl":"scrawlPathFormat",
        "uploadvideo":"videoPathFormat"
    }

    outputpath = ueditor_config.get(upload_path_format.get(action, None), "/upload/excption")
    log.debug(action,outputpath)
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    outputfilename = get_file_name(upload_original_ext)
    filepath = os.path.join(outputpath, outputfilename)
    
    
    if action in ('uploadscrawl'):
        base64data = request.form[upload_field_name]  # 这个表单名称以配置文件为准
        img = base64.b64decode(base64data)
        # 这里保存文件并返回相应的URL
        state = save_upload_file(img, filepath)
    else:
        try:
            upfile.save(filepath)
        except Exception as E:
            state = "写入文件错误:"+ str(E)

    state = "SUCCESS"
    if state == "SUCCESS":
        result = {
        "state":state,
        "url":filepath,
        "size":0,
        "title":upload_file_name,
        "original":upload_file_name,
        "source":""
        }

    return jsonify(result)

@main.route('/home')
@login_required
def home():
    
    return render_template("home.html")


@main.route('/')
@login_required
def index():
    
    return render_template("home.html")


@main.route('/blog')
@login_required
def blog():
    return render_template("blog.html")

@main.route('/life')
@login_required
def life():
    return render_template("life.html")

@main.route('/about')
@login_required
def about():
    return render_template("about.html", tips = "tips")

@main.route('/write')
@login_required
def write_blog():
    return render_template("write.html")
