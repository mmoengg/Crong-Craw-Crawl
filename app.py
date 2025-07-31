from flask import Flask, render_template
import requests
import pandas as pd
from bs4 import BeautifulSoup

app = Flask(__name__)

# --- 금천구립도서관 ---
def crawl_gc_book():
    url = 'https://geumcheonlib.seoul.kr/geumcheonlib/uce/programList.do?selfId=1090'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # 제목 행 제외

    data = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        input_tag = row.find('input', id='BOA_IDX')
        input_id = input_tag.get('value', '') if input_tag else ''
        if cols:
            category = cols[1] # 대상
            title = cols[0]  # 제목
            if category == '성인':
                # '성인'인 경우만 추가
                selected_cols = [title, input_id]
                data.append(selected_cols)

    columns = ['제목', '게시글아이디']
    df = pd.DataFrame(data, columns=columns)
    return df

# --- 금천 가족센터 ---
def crawl_gc_family(max_page=3, rows=5):
    url = 'https://geumchfc.familynet.or.kr/center/lay1/program/S295T322C451/recruitReceipt/list.do'
    headers = {'User-Agent': 'Mozilla/5.0'}

    data = []
    for page in range(1, max_page + 1):
        params = {'rows': rows, 'cpage': page}
        response = requests.get(url, headers=headers, params=params)  # 페이지별 요청
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('li.clearfix')
        if not items:
            print(f"Page {page}: 데이터 항목을 찾지 못했어요.")
            continue

        for item in items:
            a_tag = item.find('a')
            title = a_tag.get_text(strip=True) if a_tag else ''
            link = a_tag['href'] if a_tag and 'href' in a_tag.attrs else ''
            data.append([title, link])

    columns = ['제목', '링크']
    df = pd.DataFrame(data, columns=columns)
    return df

# --- 양천 가족센터 ---
def crawl_yc_family(max_page=3, rows=5):
    url = 'https://ychc.familynet.or.kr/center/lay1/program/S295T322C451/recruitReceipt/list.do'
    headers = {'User-Agent': 'Mozilla/5.0'}

    data = []
    for page in range(1, max_page + 1):
        params = {'rows': rows, 'cpage': page}
        response = requests.get(url, headers=headers, params=params)  # 페이지별 요청
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('li.clearfix')
        if not items:
            print(f"Page {page}: 데이터 항목을 찾지 못했어요.")
            continue

        for item in items:
            a_tag = item.find('a')
            title = a_tag.get_text(strip=True) if a_tag else ''
            link = a_tag['href'] if a_tag and 'href' in a_tag.attrs else ''
            data.append([title, link])

    columns = ['제목', '링크']
    df = pd.DataFrame(data, columns=columns)
    return df

# --- 강서 가족센터 ---
def crawl_gs_family(max_page=3, rows=5):
    url = 'https://gsfc.familynet.or.kr/center/lay1/program/S295T322C451/recruitReceipt/list.do'
    headers = {'User-Agent': 'Mozilla/5.0'}

    data = []
    for page in range(1, max_page + 1):
        params = {'rows': rows, 'cpage': page}
        response = requests.get(url, headers=headers, params=params)  # 페이지별 요청
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('li.clearfix')
        if not items:
            print(f"Page {page}: 데이터 항목을 찾지 못했어요.")
            continue

        for item in items:
            a_tag = item.find('a')
            title = a_tag.get_text(strip=True) if a_tag else ''
            link = a_tag['href'] if a_tag and 'href' in a_tag.attrs else ''
            data.append([title, link])

    columns = ['제목', '링크']
    df = pd.DataFrame(data, columns=columns)
    return df


# --- 라우터 ---
@app.route('/')
def home():
    df = crawl_gc_book()
    notices = df.to_dict(orient='records')  # 리스트 딕셔너리 형태로 변환
    return render_template('index.html', notices=notices)

@app.route('/gcbook')
def gcbook():
    df = crawl_gc_book()
    notices = df.to_dict(orient='records')  # 리스트 딕셔너리 형태로 변환
    return render_template('gcbook.html', notices=notices)

@app.route('/gcfamily')
def gcfamily():
    df = crawl_gc_family()
    notices = df.to_dict(orient='records')  # 리스트 딕셔너리 형태로 변환
    return render_template('gcfamily.html', notices=notices)

@app.route('/ycfamily')
def ycfamily():
    df = crawl_yc_family()
    notices = df.to_dict(orient='records')  # 리스트 딕셔너리 형태로 변환
    return render_template('ycfamily.html', notices=notices)

@app.route('/gsfamily')
def gsfamily():
    df = crawl_gs_family()
    notices = df.to_dict(orient='records')  # 리스트 딕셔너리 형태로 변환
    return render_template('gsfamily.html', notices=notices)


if __name__ == "__main__":
    app.run(debug=True)

