import os
import re
import json
import hashlib
import datetime

import flask
import flask_cors
import flask_login

from classes.user import User



## CONSTANTS
DESINENZE_COMUNI = {
    "mente"
}



## KEYS
f = open("keys/secretkey.txt",mode="r",encoding="utf-8")
skey = f.read().strip()
f.close()



## START SERVER
app = flask.Flask(__name__)
app.secret_key = skey.encode('UTF-8')

flask_cors.CORS(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)



## USER MANIPULATION
# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.get_from_id(user_id)


# Login and logout
@app.post("/login")
def login():
    # Grab login form
    login_form = flask.request.form

    username = login_form["username"]
    password = login_form["password"]

    # Validate username and password
    user = User.authenticate_user(username,password)
    if user == None:
        return flask.abort(400)

    # Finalize login
    flask_login.login_user(user)
    return flask.redirect(flask.url_for('get_root'))

@app.post("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('get_root'))

@app.post("/set_password")
@flask_login.login_required
def set_password():
    # Grab login form
    login_form = flask.request.form

    old_password = login_form["old_password"]
    new_password = login_form["new_password"]

    result = User.change_password(flask_login.current_user,old_password,new_password)
    if result == True:
        return "OK",200
    else:
        return flask.abort(401)

@app.post("/signup")
def create_new_user():
    
    # Grab login form
    login_form = flask.request.form

    username = login_form["username"]
    password = login_form["password"]

    print("ok 1")

    # Try to create the user
    result = User.create_user(username,password)

    print("ok 2")

    if result == True:
        print("ok 3")
        return flask.redirect(flask.url_for('get_root'))
    else:
        print("ok 4")
        return flask.abort(401)


@app.get("/users/<user_id>")
def get_userpage(user_id):

    # Logged in?
    logged_in = False
    user_info = None
    if flask_login.current_user.is_authenticated:
        logged_in = True
        user_info = flask_login.current_user

    if logged_in:
        return flask.render_template("private_userpage.html.jinja",user_info=user_info)
    else:
        return flask.abort(401)


@app.get("/signup")
def get_newuserpage():
    return flask.render_template("signup.html.jinja")



## CONTROLLER
# Root
@app.get("/")
def get_root():

    # Logged in?
    logged_in = False
    user_info = None
    if flask_login.current_user.is_authenticated:
        logged_in = True
        user_info = flask_login.current_user

    return flask.render_template("root.html.jinja",logged_in=logged_in,user_info=user_info)
    # Use jinja2 for template


# Analisi del testo
@app.post("/analyzeText")
def post_analyze_text():

    text_input = flask.request.form["textInput"]

    text_statistics = dict()
    worktext = text_input
    worktext = re.sub("\\W+"," ",worktext)
    for word in worktext.split(" "):
        word = word.lower()
        #print(word)
        if word not in text_statistics:
            text_statistics[word] = 0
        text_statistics[word] += 1

        # Desinenza comune?
        for desin in DESINENZE_COMUNI:
            if word.endswith(desin) and word!=desin:
                desin = "-"+desin
                if desin not in text_statistics:
                    text_statistics[desin] = 0
                text_statistics[desin] += 1

    text_output = text_input.replace("\n","<br>")
    text_dictionary = list()
    for word in text_statistics:
        if (text_statistics[word]>1):
            text_dictionary.append({"key":word, "count":str(text_statistics[word])})
    text_dictionary.sort(key=lambda i: int(i["count"]), reverse=True)

    f=open(file="logs/"+str(hashlib.md5(text_input.encode('utf-8')).hexdigest())+".txt",mode="w",encoding="utf-8")
    f.write(str(flask.request.remote_addr))
    f.write("\n")
    f.write(str(datetime.datetime.now()))
    f.write("\n----\n")
    f.write(str(text_input.replace("\r","\n").replace("\n\n","\n")))
    f.close()

    return flask.render_template("analyze_text.html.jinja", displayed_text=text_output, text_dictionary=text_dictionary)
