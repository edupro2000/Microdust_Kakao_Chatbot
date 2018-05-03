import pymongo
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")

#error messages 라는 database 생성
db = client.error_messages

#error message database에 messages라는 document 생성
message = db.messages

def save_messages(user_key, content) :
    date = datetime.datetime.utcnow()
    #한국시간으로 전환
    time_gap = datetime.timedelta(hours=9)
    date = (date + time_gap).strftime("%Y-%m-%d %H:%M:%S")
    post = {
    "user" : user_key,
    "text" : content,
    "date" : date,
    }
    message.insert_one(post) 
