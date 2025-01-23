from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import csv

# 자동화 감지를 막기 위해서 3~5 사이 랜덤 숫자를 뽑는다.
random_sec = random.uniform(3,5)
#셀레니움 4버전부터 executable_path라는 경로 대신에 Service객체를 생성해서 드라이버로 경로를 넘기는 방식으로 바뀜
#왜 이렇게 바뀌었는지 따로 정리 해놓기 
service = Service("/Users/gimhyeonseong/Downloads/chromedriver-mac-arm64/chromedriver")

driver = webdriver.Chrome(service=service)

search_url="https://www.naver.com"
driver.get(search_url)

time.sleep(random_sec)

#네이버 검색창에 "키워드" 검색
search_box = driver.find_element(By.NAME,"query")
search_box.send_keys("동탄 맛집")
search_box.send_keys(Keys.RETURN)

time.sleep(random_sec)

#검색 결과 화면에서 블로그 카테고리로 이동
#셀레니움의 요소 찾는 방식 중 하나 XPATH //a-> 현재 문서 어디에서든 a태그를 찾는다. [@role='tab']그 중에서도 role속성이 tab인 요소
#and 로 한가지 조건을 더 추가 한다. contains(param1 , param2) param1(전체문자열)에서 param2(부분문자열)을 포함하는지 여부를 체크한다.
blog_category = driver.find_element(By.XPATH,"//a[@role='tab' and contains(text(),'블로그')]")
blog_category.click()

time.sleep(random_sec)

#네이버 블로그 카테고리를 눌러 들어온 페이지에서 제목들을 추출해온다. -> 이런경우는 자주 바뀔 수 있으니 추후에 방법을 고민해본다.
titles = driver.find_elements(By.CSS_SELECTOR,".title_area a.title_link")
blog_data = []

for title in titles:
    blog_title = title.get_attribute("textContent")
    blog_url = title.get_attribute("href")
    blog_data.append({"title": blog_title, "url": blog_url})

# 데이터 출력
for item in blog_data:
    print(f"제목: {item['title']}, URL: {item['url']}")


#Python에서는 open()함수는 파일이 없으면 만들고 있으면 열어준다.
with open("dongtan_blog_data.csv","w",encoding="utf-8",newline="") as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=["title","url"])
    writer.writeheader()
    writer.writerows(blog_data)

time.sleep(random_sec)


driver.quit()
