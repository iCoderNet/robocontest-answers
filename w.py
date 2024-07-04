import requests, html, json
from bs4 import BeautifulSoup

'''
BU FILE ROBOCONTEST AKKOUNTINGIZGA JAVOBLARNI YUKLAYDI
COOKIE QO'YING, O'ZI YUKLAB CHIQADI
'''
COOKIE = "ROBOCONTEST.UZ - Full Cookies"


def show_answer(test: int):
    try:
        with open(f"tests/{test}.json", "r") as f:
            data = f.read()
            data_json = json.loads(data)
            code = data_json["code"]
            lang = data_json["lang"]
            return code, lang
    except:
        return False, False
        

def send_post_request(test: int, session: requests.Session, _token: str, form_url: str):
    code, lang = show_answer(test)
    if not code or not lang:
        print(f"TEST: {test} | LANG: {lang} | ERROR")
        return
    
    payload = {
        "_token": _token,
        "code": code,
        "language_id": lang,
    }

    response = session.post(form_url, data=payload, allow_redirects=False)

    print(response.status_code)
    print(f"TEST: {test} | LANG: {lang} | ACCEPTED")
    


def make_request(test=1):
    global COOKIE
    url = f"https://robocontest.uz/tasks/{str(test).zfill(4)}"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": COOKIE,
        "Referer": "https://robocontest.uz/tasks",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": "\"Android\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        form_url = soup.find('form', {'method': 'post'})
        _token = soup.find('input', {'type': 'hidden', 'name': '_token'})
        if form_url and _token:
            form_url = form_url.get('action')
            _token = _token.get('value')
            send_post_request(test, session, _token, form_url)
        else:
            print("ERROR", test)
    else:
        print("Failed to make request. Status code:", response.status_code)

h = 0
for i in range(712, 1213):
    make_request(i)
    h += 1
    import time
    if h % 3 == 0:
        time.sleep(20)
    time.sleep(10)
