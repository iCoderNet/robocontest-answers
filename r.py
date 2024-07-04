import requests, html
from bs4 import BeautifulSoup

'''
BU FILE ROBOCONTEST SAYTIDAN JAVOBLARNI NUSXA QILADI
COOKIE QO'YING, O'ZI KO'CHIRIB OLADI
'''
COOKIE = "ROBOCONTEST.UZ - Full Cookies"


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

    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        td_tag = soup.find('td', {'data-attempt-status': '', 'class': 'text-success text-center', 'nowrap': ''})
        if td_tag:
            # languages_data = soup.find('code-submit')[':languages']
            # languages = eval(html.unescape(languages_data))

            # Extract the last attempt data
            last_attempt_data = soup.find('code-submit')[':last-attempt']
            last_attempt = html.unescape(last_attempt_data)
            
            with open(f'tests/{test}.json', 'w', encoding='utf-8') as f:
                f.write(last_attempt)
            print(td_tag.text.strip(), test)
        else:
            print("ERROR", test)
    else:
        print("Failed to make request. Status code:", response.status_code)

# Call the function to make the request
for i in range(156, 1213):
    import time
    time.sleep(0.2)
    make_request(i)