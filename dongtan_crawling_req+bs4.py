import requests #웹 사이트에 HTTP 요청을 보낼 수 있게 도와주는 라이브러리 
from bs4 import BeautifulSoup #HTML , XML을 파싱해서 원하는 정보를 찾게 해준다.
import csv #csv파일을 읽고 쓰게 해주는 기능을 제공해준다.
import random 
import time

# 자동화 판단으로 인한 IP 차단을 막기 위해서 random 숫자를 사용
def random_sleep(min_sec=3,max_sec=5):
    sec = random.uniform(min_sec,max_sec) #float 난수를 반환한다.
    time.sleep(sec)

#셀레니움에서는 네이버 메인페이지에서 검색창에 키워드를 입력 후 검색이 가능했지만 request+bs4 기능을 통해 다이렉트로 검색 페이지 이동이 가능하다.
search_url = "https://search.naver.com/search.naver"
set_params = {
    "query":"동탄 맛집",
    "where":"nexearch"
}

#봇 트래픽 감지에 걸리지 않기 위해 실제 브라우저에서 보내는거처럼 설정 하기 
set_headers = {
    "User-Agent":(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/108.0.0.0 Safari/537.36"
    )
}

random_sleep()

#네이버 서버로 요청을 보내서 응답 객체를 받는다.
response = requests.get(search_url, params=set_params,headers=set_headers)

#응답 객체에서 text속성을 추출한다.
html = response.text

#html 태그를 파싱한다.
soup = BeautifulSoup(html,"html.parser")
# print(soup.prettify())
# print(soup.find_all("a"))
print(soup.find("a",{"role":"tab"}).prettify())
print()
print(response.status_code)

#soup객체에서 태그를 검색하고 텍스트를 추출한다.
#find 메서드를 통해 HTML태그를 찾는다.(여기서 a태그) -> 찾은 태그 에서 HTML 속성으로 설정된 태그를 찾는다.(여기서 role="tab") -> 설정한 문자열이 있다면 true 없으면 false
#파이썬 람다 함수는 lambda 매개변수:조건 으로 작성한다.
blog_tab = soup.find("a",{"class":"tab"})
## 위 코드에서 자꾸 None이 반환되어서 추후에 문제점을 찾아서 보완할 예정이다.


if blog_tab is None:
    print("블로그 탭을 찾지 못했습니다. (HTML 구조 확인 요망)")
    exit()

#selenium으로 치면 블로그 탭을 클릭할 URL 작성
href = blog_tab.get("href")
print(href)
blog_tab_url="https://search.naver.com/search.naver"+href
random_sleep()
blog_response = requests.get(blog_tab_url,headers=set_headers)

#블로그 탭을 클릭해서 나온 화면의 HTML 문서 로드
blog_tab_html = blog_response.text
blog_soup = BeautifulSoup(blog_tab_html,"html.parser")

#title_area 클래스에서  a태그 중에서 title_link클래스를 가져온다. 
title_links = blog_soup.select(".title_area a.title_link")


blog_data = []

for link in title_links:
    #strip은 양쪽 공백을 제거하는 기능이다.
    title_text = link.get_text(strip=True)
    url_link = link.get("href")
    blog_data.append({"title":title_text,"url":url_link})


print("\n================ 추출한 블로그 글 ===================")
for item in blog_data:
    print(f"제목{item['title']}  ||  URL: {item['url']}")

file_name = "dongtan_blog_data.csv"

with open(file_name,"w",encoding="utf-8",newline="") as csvfiles:
    writer = csv.DictWriter(csvfiles,fieldnames=["title","url"])
    writer.writeheader()
    writer.writerows(blog_data)


print(f"\n총 {len(blog_data)}건의 데이터를 '{file_name}' 파일로 저장했습니다.")
