import requests
from bs4 import BeautifulSoup

#미세먼지 및 초미세먼지 농도별 등급 판정
def micro_grade(num) : 
    if num >=0 and num <= 30 : 
        result = "좋음"
    elif num > 30 and num <= 80 :
        result = "보통"
    elif num > 80 and num <= 150 : 
        result = "나쁨"
    else :
        result = "매우나쁨"
    return result

def nano_grade(num) : 
    if num >=0 and num <= 15 : 
        result = "좋음"
    elif num > 15 and num <= 35 :
        result = "보통"
    elif num > 35 and num <= 75 : 
        result = "나쁨"
    else :
        result = "매우나쁨"
    return result



servicekey = "u4Q%2FF%2BzFS1PHRIhVj2cJcxGP8J%2B5vOxCbaO039frcCGDEuD2km6rhbR2wZrwBrZtlLu2Z%2FbsqMHDVVGHwkq8ow%3D%3D" 
def microdust_1(loc) : 
    try :
        url = " http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName="+loc+"&dataTerm=month&pageNo=1&numOfRows=10&ServiceKey="+servicekey+"&ver=1.3"
        response = requests.get(url)
        dom = BeautifulSoup(response.content, "html.parser")
        date = dom.select("datatime")[0].text
        pm10 = int (dom.select("pm10value")[0].text)
        pm25 = int(dom.select("pm25value")[0].text)
        result = '''현재 시간 : {} 
		현재 미세먼지 농도 : {}({}) 
		현재 초 미세먼지 농도 : {}({})'''.format(date, pm10, micro_grade(pm10),  pm25, nano_grade(pm25))
    except Exception :
        result = "몰라 니가 알아봐"
    return result

