import os
import re
import json
import hashlib
import datetime

from flask import Flask
from flask import escape
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS



# CONSTANTS
DESINENZE_COMUNI = {
    "mente"
}



## START SERVER
app = Flask(__name__)
CORS(app)



## CONTROLLER
# Root
@app.get("/")
def get_root():
    return render_template("root.html.jinja")#, variable=variable)
    # Use jinja2 for template



# Analisi del testo
@app.post("/analyzeText")
def post_analyze_text():

    text_input = request.form["textInput"]

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
    f.write(str(request.remote_addr))
    f.write("\n")
    f.write(str(datetime.datetime.now()))
    f.write("\n----\n")
    f.write(str(text_input.replace("\r","\n").replace("\n\n","\n")))
    f.close()

    return render_template("analyze_text.html.jinja", displayed_text=text_output, text_dictionary=text_dictionary)