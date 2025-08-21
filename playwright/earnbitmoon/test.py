import base64
import requests
import time

def image_to_base64(path="captcha.png"):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
captcha = image_to_base64()
print(captcha)

def imgToText(key, method, body):
    url = "https://api.sctg.xyz/in.php"
    payload = {
        "key": key,
        "method": method,
        "body": body
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    print(response.text)

    result_id= int(response.text.split('|')[1].strip())
    print(result_id)
    time.sleep(5)
    url = f"https://api.sctg.xyz/res.php?key={key}&id={result_id}&action=get"
    response = requests.get(url)
    print(response.text)

    return response.text.split('|')[1].strip()

imgToText('IRLgD0hHa8dNh4hNMuG3nJuWoXjKir9x','base64',captcha)
