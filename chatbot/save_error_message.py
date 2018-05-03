import pymongo
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")

#error messages 라는 database 생성
db = client.error_messages

#error message database에 messages라는 document 생성
message = db.messages

def save_messages(user_key, content) :  
    date = datetime.datetime.utcnow()
    date = date.strftime("%A %d. %B %Y")
    post = {
    "user" : user_key,
    "test" : content,
    "date" : date,
    }
    message.insert_one(post) 
