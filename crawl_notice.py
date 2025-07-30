import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 금천구립도서관 공지사항 크롤링 함수
def crawl_geumcheon_notice():
    url = 'https://geumcheonlib.seoul.kr/geumcheonlib/uce/board/noticeList.do?selfId=1082'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # 제목 행 제외
    
    data = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        if cols:
            data.append(cols)
    
    columns = ['번호', '제목', '작성자', '파일', '등록일', '조회수']
    df = pd.DataFrame(data, columns=columns)
    df['출처'] = '금천구립도서관'
    return df

# 2. 양천구 가족센터 행사 리스트 크롤링 함수 (최대 3페이지까지 예시)
def crawl_yangcheon_events(max_page=3):
    base_url = "https://ychc.familynet.or.kr/center/lay1/program/S295T322C451/recruitReceipt/list.do"
    headers = {'User-Agent': 'Mozilla/5.0'}
    rows = 5

    all_data = []
    for page in range(1, max_page + 1):
        params = {'rows': rows, 'cpage': page}
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.select('li.clearfix')
        if not items:
            print(f"Page {page}: 데이터 항목을 찾지 못했어요.")
            continue
        
        for item in items:
            a_tag = item.find('a')
            title = a_tag.get_text(strip=True) if a_tag else ''
            all_data.append([title])

    df = pd.DataFrame(all_data, columns=['제목'])
    df['출처'] = '양천구 가족센터'
    return df

# 3. 각 크롤러 실행 및 데이터 합치기
df_geumcheon = crawl_geumcheon_notice()
df_yangcheon = crawl_yangcheon_events()

# 양천구 데이터에는 '번호', '작성자', '파일', '등록일', '조회수' 칼럼 없으니 빈 칼럼 추가
for col in ['번호', '작성자', '파일', '등록일', '조회수']:
    df_yangcheon[col] = '-'

# 금천구 데이터에서 '번호', '파일', '등록일', '조회수' 컬럼 제거 (불필요하므로)
df_geumcheon = df_geumcheon.drop(columns=['번호', '파일', '등록일', '조회수'])

# 양천구도 불필요한 컬럼 제거 ('번호'는 이미 빈 칼럼이므로 제거)
df_yangcheon = df_yangcheon.drop(columns=['번호', '파일', '등록일', '조회수'])

# 두 데이터 프레임에서 '작성자' 컬럼은 남겨두거나 필요없으면 삭제해도 됨
# 아래는 '작성자'도 제거하길 원하면 이 줄 추가
# df_geumcheon = df_geumcheon.drop(columns=['작성자'])
# df_yangcheon = df_yangcheon.drop(columns=['작성자'])

# 컬럼 정리 후 출처, 제목, 작성자 정도만 남기려면 이렇게 진행
columns_order = ['제목', '작성자', '출처']
# 양쪽 데이터프레임 컬럼 순서 맞추기
df_geumcheon = df_geumcheon[columns_order]
df_yangcheon = df_yangcheon[columns_order]

# 두 데이터 합치기
df_all = pd.concat([df_geumcheon, df_yangcheon], ignore_index=True)

# '제목'에 '공지'라는 단어가 포함된 행 제거
df_all = df_all[~df_all['제목'].str.contains('공지')].reset_index(drop=True)

# 결과 출력
print(df_all)