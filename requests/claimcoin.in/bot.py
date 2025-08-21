import requests, time, os, base64
from bs4 import BeautifulSoup

def dataRead():
    try:
        with open('data.txt','r',encoding='utf-8') as f:
            user_agent, cookie_str = f.readlines()
    except:
        print(f'________________________________________')
        user_agent = input('>> Input UserAgent: ')
        cookie_str = input('>> Input Cookie: ')
        print(f'________________________________________')
        with open('data.txt','w',encoding='utf-8') as f:
            f.write(f'{user_agent}\n{cookie_str}')
    return user_agent.strip() , cookie_str.strip()


def cookie_str_to_dict(cookie_str: str) -> dict:
    cookies = {}
    for item in cookie_str.split(";"):
        if "=" in item:
            k, v = item.strip().split("=", 1)
            cookies[k] = v
    return cookies


user_agent, cookie_str = dataRead()
cookies = cookie_str_to_dict(cookie_str=cookie_str)
headers = {
    'User-Agent': user_agent
}

r = requests.get('https://claimcoin.in/faucet',headers=headers,cookies=cookies)
print(r.status_code)
with open('respone.txt','w',encoding='utf-8') as f:
    f.write(r.text)

soup = BeautifulSoup(r.text, 'html.parser')

test = soup.find_all("a", attrs={"rel": True})

for i in test:
    print(i)
    print()