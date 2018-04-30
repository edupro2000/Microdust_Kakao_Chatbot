# -*- coding: utf-8 -*-

#---------------------------------
# quizbot.py
#---------------------------------



import os
from flask import Flask, request, jsonify
from test import microdust_1


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

    if content == "미세먼지" :

        dataSend = {"message": {"text": "미세먼지를 알려준다. **동만 말해."}}

    elif "동" in content :

        dataSend = {"message": {"text": microdust_1(content)}}

		
    elif "안녕" in content :

        dataSend = {"message":{"text": "이것도 되는가"}}

    else :
        dataSend = {"message": {"text": "시키지 않은 것 하지마라"}}

    return jsonify(dataSend)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
