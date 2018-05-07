# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify
from Total_Functions import *
from save_error_message import save_messages


app = Flask(__name__)



@app.route('/keyboard')
def Keyboard():

    dataSend = {
        "type" : "buttons",
        "buttons" : ["미세먼지를 알려줘"]
    }

    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    user_key = dataReceive['user_key']
    save_messages(user_key, content)
    if content == "미세먼지를 알려줘" or content == "다른 지역 미세먼지를 알려줘" :

        dataSend = {
            "message":
            {
            "text": '''지역명만 알려주시면 실시간으로 미세먼지를 알려드려요! 대화형 챗봇이 아닙니다! 
       상도역, 강남 교보문고 처럼 입력해주세요!'''
            }
                   }

    else :
        list_of_places = check_detail(content)
        place = get_microdust(content)
        if len(list_of_places) > 1 :
            dataSend = {
                "message" :
                {
                    "text" : "중복되는 지명입니다! 어느 곳인지 지정해주세요!"
                },
                "keyboard" : {
                    "type" : "buttons",
                    "buttons" : list_of_places,
                }
            }
        elif "오타" not in place: 
            dataSend = {
                "message" : 
                {
                    "text" : place
                }
            }
        else : 
            dataSend = {
                "message" : 
                {
                    "text" : "다시 입력해주세요."
                }
            }

    return jsonify(dataSend) 



if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
