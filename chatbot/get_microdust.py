
# coding: utf-8

# ## 한국환경공단 대기오염 API를 이용한 미세먼지 데이터 가져오기

# In[2]:


import requests
from bs4 import BeautifulSoup
import pickle


# In[68]:


#미세먼지 및 초미세먼지 농도별 등급 판정
def grade(num) : 
    try :
        num = int(num)
        if num >=0 and num <= 30 : 
            result = "좋음"
        elif num > 30 and num <= 80 :
            result = "보통"
        elif num > 80 and num <= 150 : 
            result = "나쁨"
        else :
            result = "매우나쁨"
    except : 
        result = "-"
    return result

def nano_grade(num) : 
    try : 
        if num >=0 and num <= 15 : 
            result = "좋음"
        elif num > 15 and num <= 35 :
            result = "보통"
        elif num > 35 and num <= 75 : 
            result = "나쁨"
        else :
            result = "매우나쁨"
    except : 
        result = "-"
    return result


# ---------

# ## 1. 측정소 정보 조회
# - 대기질 측정소 정보를 조회하기 위해 TM 좌표 기반의 가까운 측정소 및 측정소 목록과 측정소의 정보를 조회할 수 있음.

# In[4]:


with open('get_tm_coor_key.txt', 'rb') as f :
    get_tm_coor_key = pickle.load(f)


# In[84]:


def get_tm_coor(loc) : 
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/MsrstnInfoInqireSvc/getTMStdrCrdnt?umdName="+ loc +"&pageNo=1&numOfRows=10&ServiceKey=" + get_tm_coor_key
    response = requests.get(url)
    dom = BeautifulSoup(response.content, "html.parser")
    count = int(dom.select("totalcount")[0].text)
    
    if count == 0 :
        
        result = "없는 지역입니다. 다시 입력해 주세요.", None
        
    else : 
        
        X = dom.select("tmx")[0].text
        Y = dom.select("tmy")[0].text
        result = X, Y
        
    return result


# In[38]:


get_tm_coor("영통동")


# -----------

# ## TM 기준좌표 조회
# - 검색서비스를 사용하여 읍면동 이름을 검색조건으로 기준좌표 (TM좌표)정보를 제공하는 서비스

# In[40]:


with open("tm_station_key.txt", "wb") as f :
    pickle.dump(tm_station_key, f)


# In[41]:


with open("tm_station_key.txt", "rb") as f :
    tm_station_key = pickle.load(f)


# In[43]:


def nearest_station(X, Y) : 
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/MsrstnInfoInqireSvc/getNearbyMsrstnList?tmX=    " + X + "&tmY=" + Y +"&pageNo=1&numOfRows=10&ServiceKey=" + tm_station_key
    response = requests.get(url)
    dom = BeautifulSoup(response.content, "html.parser")
    name = dom.select("stationname")[0].text
    distance = dom.select("tm")[0].text
    return name, distance + "km"


# In[44]:


X, Y = get_tm_coor("병점동")


# In[45]:


nearest_station(X, Y)


# --------

# In[48]:


servicekey_1 = "u4Q%2FF%2BzFS1PHRIhVj2cJcxGP8J%2B5vOxCbaO039frcCGDEuD2km6rhbR2wZrwBrZtlLu2Z%2FbsqMHDVVGHwkq8ow%3D%3D" 


# In[91]:


def microdust_1(loc) : 
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName="+loc+"&dataTerm=month&pageNo=1&numOfRows=10&ServiceKey="+servicekey_1+"&ver=1.3"
    response = requests.get(url)
    dom = BeautifulSoup(response.content, "html.parser")
    date = dom.select("datatime")[0].text
    pm10 = dom.select("pm10value")[0].text
    pm25 = dom.select("pm25value")[0].text
    result = '''현재 시간 : {} 
    현재 미세먼지 농도 : {}({}) 
    현재 초 미세먼지 농도 : {}({})'''.format(date, pm10, grade(pm10),  pm25, nano_grade(pm25))
    return result


# In[92]:


place = "부산 해운대"
def get_microdust(place) : 
    try : 
        X, Y = get_tm_coor(place)
        name, distance = nearest_station(X, Y)
        result = microdust_1(name)
    except : 
        result = "오류 발생"
    return result


# In[93]:


get_microdust("해운대")

