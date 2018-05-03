# -*- coding: utf-8 -*-

#---------------------------------
# quizbot.py
#---------------------------------



import os
from flask import Flask, request, jsonify
from get_microdust import *
from save_error_message import save_messages


app = Flask(__name__)



@app.route('/keyboard')
def Keyboard():

    dataSend = {
        "type" : "buttons",
        "buttons" : [u"미세먼지"]
    }

    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():

    dataReceive = request.get_json()
    content = dataReceive['content']
    user_key = dataReceive['user_key']

    if content == "미세먼지" :

        dataSend = {"message": {"text": "사는 지역을 알려주시면 실시간으로 미세먼지를 알려드려요!"}}

    elif "동" in content :

        dataSend = {"message": {"text": get_microdust(content) } }

		
    elif "안녕" in content :

        dataSend = {"message":{"text": dataReceive } }

    else :
        save_messages(user_key, content)
        dataSend = {"message": {"text": "더 공부해서 오겠습니다.."}}

    return jsonify(dataSend)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
