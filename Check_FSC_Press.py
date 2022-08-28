# 금융위원회 최신 보도자료를 텔레그램으로 보내기('21년도 1월 홈페이지 개편 후)
# filename : CheckFSCPress_v1.py
# 개발언어 : Python 3
# 버전 :  1.0
# 최종 작성일 : 2021. 1. 13.
# 사전 준비물 : 
#      1) 텔레그램 봇(Bot API Token)  
#      2) 텔레그램 채널(@PressNews2018Channel)

import requests
from bs4 import BeautifulSoup
import urllib, urllib3

urllib3.disable_warnings()
http = urllib3.PoolManager()

URL = "http://www.fsc.go.kr/no010101"
DOMAIN = "https://www.fsc.go.kr"

filename = 'LatestNoFSC.txt'

# 파일에서 게시물 번호 가져오기
def GetTheNoFromFile():
    input_file = open(filename, 'r')
    fileNo = input_file.readline()
    input_file.close()
    return(fileNo)
    
# 최신 게시물번호를 파일에 덮어쓰기 
def UpdateTheNewNo(strNewNo):
    output_file = open(filename, 'w')
    output_file.write(strNewNo)
    output_file.close()

# 2차원 배열(box) 선언과 초기화
box = [['','',''],['','',''],['','',''],['','',''],['','',''],
       ['','',''],['','',''],['','',''],['','',''],['','','']]    

# 파일에서 게시물번호를 전역변수 NoFromFile에 저장(리턴값:fileNo)
NoFromFile = GetTheNoFromFile()    
    
response = requests.get(URL)
dom = BeautifulSoup(response.content, "html.parser")
title_links = dom.select(".subject a")
num_links = dom.select(".count")

for i in range(10):
    box[i][0] = num_links[i].text
    box[i][1] = title_links[i].text + '\n'
    box[i][2] = title_links[i]['href'].split('?')[0]

# 현재 게시판의 최신 게시물 번호 저장      
lastNo = int(box[0][0])

# 홈페이지의 최신 게시물번호와 파일의 게시물번호의 차이 구하기
j = int(lastNo) - int(NoFromFile) - 1
    
# 최신 게시물 정보만 골라서 텔레그램으로 발송
for i in range(j, -1, -1):

    # title_URL 앞에 DOMAIN 붙이기    
    strURL = DOMAIN + box[i][2]

    # 홈페이지에서 가져온 해당 게시물번호(정수형)를 변수에 저장
    strNumber = str(box[i][0])    

    # 새 번호로 파일내용 업데이트
    # UpdateTheNewNo(strNumber)

    # 텔레그램으로 보내기(보도자료 알람 @PressNews2018Channel)
    Teleg_URL = "https://api.telegram.org/bot777777777:AAAAAAAAAAAAA_BBBBBBBBBBBBBBBBBBBBB/sendMessage?chat_id=@PressNews2018Channel&text="

    strTelMsg = '{}{}{}{}'.format(Teleg_URL, urllib.parse.quote("<금융위 보도자료>\n"), 
                urllib.parse.quote(box[i][1]), urllib.parse.quote(strURL))
    http.request('GET', strTelMsg).data 

print("Done!")
