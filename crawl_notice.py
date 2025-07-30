import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://geumcheonlib.seoul.kr/geumcheonlib/uce/board/noticeList.do?selfId=1082'

headers = {
    'User-Agent': 'Mozilla/5.0'  # 접속 차단 우회를 위한 헤더
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# 공지사항 표 <table> 찾기
table = soup.find('table')
rows = table.find_all('tr')[1:]  # 타이틀 행 제외

data = []
for row in rows:
    cols = [td.get_text(strip=True) for td in row.find_all('td')]
    if cols:
        data.append(cols)

# pandas 데이터프레임 변환
columns = ['번호', '제목', '작성자', '파일', '등록일', '조회수']
df = pd.DataFrame(data, columns=columns)
print(df)  # 상위 5개 행 출력
