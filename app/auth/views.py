# _*_ coding:utf-8 _*_

from flask import render_template, redirect, request, url_for, jsonify, current_app 
from flask_login import login_user, current_user, logout_user, login_required
from logbook import Logger
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import auth
from app.models import User, RegisterUser, Captcha
from app.email import send_email

log = Logger("AUTH.VIEWS")
@auth.route("/resetPassword/save", methods=["POST"])
def save_password():
    token = request.values.get("key", None)
    password = request.values.get("password", None)
    try:
        json_data = User.parse_token(token)
    except Exception as e:
        log.error(str(e))
        return jsonify({"result":0})
    email = json_data["email"]
    user_id = RegisterUser.get_id(email)
    user = User(user_id)
    user.password = password
    url = "/auth/sign"
    return jsonify({"result": 1, "url": url})

@auth.route("/resetPassword/<token>", methods=["POST", "GET"])
def reset_password(token):
    try:
        return render_template("auth/resetpassword.html")
    except Exception as e:
        log.warning(str(e))
        return render_template("404.html"), 404

@auth.route("/forgetPassword")
def forget_password():
    return render_template("auth/verifyAccount.html")

def get_UTCDate():
    return datetime.utcnow().strftime("%Y-%m-%d")

@auth.route("/verifyCaptcha", methods=["POST"])
def verify_captcha():
    log.debug(request.form)
    captcha = request.form.get("captcha", None)
    email = request.form.get("email", None)
    action = request.form.get("action", None)
    
    Captcha_obj = Captcha()
    result = Captcha_obj.verify_captcha(email, captcha)
    log.debug(result)
    if action == "verifyAccount":
        if(result):
            token = User.generate_token({"email":email, "captcha":captcha}, 3600).decode("utf-8")
            log.debug(token)
            return jsonify({"result":1, "url": "/auth/resetPassword/" + token})
        else:
            return jsonify({"result":0})
    else:
        if(result):
            return jsonify({"result":1})
        else:
            return jsonify({"result":0})

@auth.route("/verifyUser", methods=["POST","GET"])
def verify_username():
    log.debug(request.form)
    username = request.form["username"]
    if(RegisterUser.verify_username(username)):
        return jsonify({"result":1})
    else:
        return jsonify({"result":0})

@auth.route("/verifyEmail", methods=["POST","GET"])
def verify_email():
    email = request.form["email"]
    log.debug(email)
    if(RegisterUser.verify_email(email)):
        return jsonify({"result":1})
    else:
        return jsonify({"result":0})

@auth.route("/sign", methods=["POST", "GET"])
def sign():
    return render_template("auth/sign.html")


@auth.route("/captcha", methods=["POST"])
def captcha():
    email = request.form.get("email", None)
    action = request.form.get("action", None)
    if action == "verifyAccount":
        log.debug(email)
        captcha_obj = Captcha()
        captcha = captcha_obj.generate_captcha()
        captcha_obj.save_captcha(email, captcha)
        date = get_UTCDate()
        data={"captcha":captcha,"date":date}
        send_email(email, "账户安全验证", "mail/captcha", **data )
        return jsonify({"result":1})
    else:
        log.debug(email)
        captcha_obj = Captcha()
        captcha = captcha_obj.generate_captcha()
        captcha_obj.save_captcha(email, captcha)
        date = get_UTCDate()
        data={"captcha":captcha,"date":date}
        send_email(email, "注册验证", "mail/captcha", **data )
        return jsonify({"result":1})
@auth.route("/signin", methods=["POST"])
def signin():
    log.debug(request.form)
    input_email = request.form.get("inputEmail",None)
    input_password = request.form.get("inputPassword", None)
    remember_me = request.form.get("remember_me", "0")
    if remember_me == "1":
        remember_me = True
    else:
        remember_me = False
    log.debug(RegisterUser.verify_email(input_email))
    if(RegisterUser.verify_email(input_email) is False):
        user = User(RegisterUser.get_id(input_email))
    
    if user.verify_password(input_password):
        login_user(user, remember = remember_me)
        return redirect(request.args.get("next") or url_for("main.home"))
    return jsonify({"result":0})

@auth.route("/signout", methods=["GET"])
@login_required
def signout():
    logout_user()
    return redirect(url_for("auth.sign"))

@auth.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username" , None)
    password = request.form.get("firstPassword", None)
    email = request.form.get("signupEmail", None)
    captcha = request.form.get("captcha", None)
    user_info = {
    "username":username,
    "password":password,
    "email":email,
    "captcha":captcha
    }
    captcha_obj = Captcha()
    if(captcha_obj.verify_captcha(email, captcha)):
        RegisterUser.register(user_info)
        return redirect(request.args.get('next') or url_for("main.home"))
    else:
        return jsonify({"result":0})
    