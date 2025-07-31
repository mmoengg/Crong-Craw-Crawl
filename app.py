from flask import Flask, render_template
import requests
import pandas as pd
from bs4 import BeautifulSoup

app = Flask(__name__)

def crawl_sing_seoul():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import time
    import pandas as pd

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://1in.seoul.go.kr/front/partcptn/partcptnListPage.do"
    driver.get(url)
    time.sleep(2)  # 데이터 로딩 대기

    rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        title = cols[2].text.strip() if len(cols) > 2 else ''
        local = cols[1].text.strip() if len(cols) > 1 else ''
        # '중장년'이 title에 포함되면 제외
        if '중장년' in title:
            continue
        data.append([title, local])

    driver.quit()

    df = pd.DataFrame(data, columns=['제목', '지역'])
    return df

# --- 금천구립도서관 ---
def crawl_gc_book():
    url = 'https://geumcheonlib.seoul.kr/geumcheonlib/uce/programList.do?selfId=1090'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)  # 타임아웃 10초 지정
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("요청 시간이 초과되었습니다. 나중에 다시 시도하세요.")
        return pd.DataFrame()  # 빈 데이터프레임 반환하거나 적절히 처리
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 에러 발생: {e}")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"요청 중 에러 발생: {e}")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]

    data = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        input_tag = row.find('input', id='BOA_IDX')
        input_id = input_tag.get('value', '') if input_tag else ''
        if cols:
            category = cols[1]
            title = cols[0]
            if category == '성인':
                if '중장년' in title:
                    continue
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


# --- 마포 가족센터 ---
def crawl_mp_family(max_page=3, rows=5):
    url = 'https://mapo.familynet.or.kr/center/lay1/program/S295T322C451/recruitReceipt/list.do'
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

@app.route('/singseoul')
def singseoul():
    df = crawl_sing_seoul()

    notices = df.to_dict(orient='records')  # 리스트 딕셔너리 형태로 변환
    return render_template('singseoul.html', notices=notices)

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

@app.route('/mpfamily')
def mpfamily():
    df = crawl_mp_family()
    notices = df.to_dict(orient='records')  # 리스트 딕셔너리 형태로 변환
    return render_template('mpfamily.html', notices=notices)


if __name__ == "__main__":
    app.run(debug=True)

