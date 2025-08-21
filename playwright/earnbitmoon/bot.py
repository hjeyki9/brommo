from playwright.sync_api import sync_playwright
from PIL import Image, ImageFilter, ImageOps
import pytesseract
import json
import base64
import requests
import time
import itertools
import sys
#=============================
#       Xevil Captcha
#=============================
def readKEY():
    try:
        with open('xevilkey.txt','r',encoding='utf-8') as f:
            API_KEY = f.readline().strip()
    except:
        API_KEY = input('Please input xevil APIKEY: ')
        with open('xevilkey.txt','w',encoding='utf-8') as f:
            f.write(API_KEY)
    return API_KEY

API_KEY = readKEY()
def image_to_base64(path="captcha.png"):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
def getbalance():
    url= f"https://api.sctg.xyz/res.php?key={API_KEY}&action=getbalance"
    response = requests.get(url=url)
    print(f'{lblack}|{lgreen}${lblack}|{lyellow} Xevil Key Balance:{lgreen} {response.text}${reset}')

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

#=============================
#       Utils Function
#=============================
def colors():
    global reset, black, red, green, yellow, blue, magenta, cyan, white, lblack, lred, lgreen, lyellow, lblue, lmagenta, lcyan, lwhite, bold, underline, reverse
    reset="\033[0m"
    black="\033[30m"
    red="\033[31m"
    green="\033[32m"
    yellow="\033[33m"
    blue="\033[34m"
    magenta="\033[35m"
    cyan="\033[36m"
    white="\033[37m"

    # bright
    lblack="\033[90m"
    lred="\033[91m"
    lgreen="\033[92m"
    lyellow="\033[93m"
    lblue="\033[94m"
    lmagenta="\033[95m"
    lcyan="\033[96m"
    lwhite="\033[97m"

    # style
    bold="\033[1m"
    underline="\033[4m"
    reverse="\033[7m"

colors()
def dataRead():
    try:
        with open('data.txt','r',encoding='utf-8') as f:
            user_agent, cookie_str = f.readlines()
    except:
        print(f'{lblack}________________________________________')
        user_agent = input('>> Input UserAgent: ')
        cookie_str = input('>> Input Cookie: ')
        print(f'{lblack}________________________________________')
        with open('data.txt','w',encoding='utf-8') as f:
            f.write(f'{user_agent}\n{cookie_str}')
    return user_agent.strip() , cookie_str.strip()

def cooldown(total_seconds: int, message: str = "", final_message: str ="                               "):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    spinner = itertools.cycle(frames)
    fps = 6
    frame_dt = 1.0 / fps
    start = time.perf_counter()
    last_len = 0

    def fmt(seconds: int) -> str:
        h, r = divmod(seconds, 3600)
        m, s = divmod(r, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    try:
        while True:
            elapsed = time.perf_counter() - start
            remaining = max(0, total_seconds - int(elapsed))  # giảm mỗi 1s
            stamp = fmt(remaining)
            out = f"{next(spinner)} {message} {stamp}".rstrip()

            # In đè cùng dòng, xử lý trường hợp độ dài ngắn/dài khác nhau
            sys.stdout.write("\r" + out + " " * max(0, last_len - len(out)))
            sys.stdout.flush()
            last_len = len(out)

            if remaining <= 0:
                break
            time.sleep(frame_dt)
    except KeyboardInterrupt:
        # Cho phép Ctrl+C thoát gọn
        pass
    finally:
        # In dòng cuối 00:00:00 + xuống dòng
        final = f"✓ 00:00:00 {final_message}".rstrip()
        sys.stdout.write("\r" + final + " " * max(0, last_len - len(final)) + "\n")
        sys.stdout.flush()


#=============================
#       Create Browser
#=============================
def parse_cookie_string(cookie_str: str, domain: str):
    """Chuyển cookie string thành list dict cho Playwright"""
    cookies = []
    for item in cookie_str.split("; "):
        if "=" in item:
            name, value = item.split("=", 1)
            cookies.append({
                "name": name.strip(),
                "value": value.strip(),
                "domain": domain,
                "path": "/"
            })
    return cookies

def create_browser(user_agent=None, cookie_str=None, domain=None):
        args = [
            "--disable-blink-features=AutomationControlled",  # tắt dấu hiệu bot
            "--mute-audio",  # tắt tiếng
            "--disable-infobars",
            "--disable-notifications",
            "--disable-popup-blocking",
            "--disable-extensions",
        ]

        browser = p.chromium.launch(headless=False, args=args)
        context = browser.new_context(
            user_agent=user_agent if user_agent else None,
            viewport={"width": 1366, "height": 768}
        )

        # Thêm cookie nếu có
        if cookie_str and domain:
            cookies = parse_cookie_string(cookie_str, domain)
            context.add_cookies(cookies)

        page = context.new_page()

        # Patch để tránh bị detect automation
        page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        """)

        return browser, context, page

#=============================
#       BOT FUNCTION
#=============================
def download_img(page, xpath, save_as="captcha.png"):
    img = page.locator(xpath)
    src = img.get_attribute("src")
    if src.startswith("data:image"):  
        # nếu ảnh là base64 inline
        import base64
        data = src.split(",")[1]
        with open(save_as, "wb") as f:
            f.write(base64.b64decode(data))
    else:
        # nếu là link ảnh bình thường
        r = requests.get(src, stream=True)
        with open(save_as, "wb") as f:
            f.write(r.content)

def save_canvas(page, xpath: str, filename: str):
    canvas = page.locator(f"xpath={xpath}")
    data_url = canvas.evaluate("(c) => c.toDataURL('image/png')")
    base64_data = data_url.split(",")[1]
    with open(filename, "wb") as f:
        f.write(base64.b64decode(base64_data))
    print(f"[+] Saved canvas -> {filename}")

def faucet(context,page):
    for i in range(3):
        click_popup = page.locator('//*[@id="app"]/div/div[3]/section/div[2]/div[2]/div/div')
        print('Trying click AdPopUp')
        click_popup.click()
        tabs = context.pages
        page = tabs[1]
        tabs[0].close()

    captcha_input = page.locator('//*[@id="app"]/div/div[3]/section/div[3]/div[1]/form/center[2]/div/input')
    captcha_input.scroll_into_view_if_needed()
    print(f'{lgreen}Scrolled to captcha')
    download_img(page, '//*[@id="Imageid"]', 'captcha.png')
    print(f'{lgreen}Saved Captcha Canvas')
    captchabase64= image_to_base64('captcha.png')
    textinput = imgToText(API_KEY,'base64',captchabase64)
    #Close POPUP 2 times
    click_popup = page.locator('//*[@id="app"]/div/div[3]/section/div[2]/div[2]/div/div')

    text_input = page.locator('//*[@id="app"]/div/div[3]/section/div[3]/div[1]/form/center[2]/div/input')
    text_input.type(textinput)
    claim = page.locator('//*[@id="app"]/div/div[3]/section/div[3]/div[1]/form/button')
    claim.scroll_into_view_if_needed()
    claim.click()
    time.sleep(1)
    status = page.locator('//*[@id="app"]/div/div[3]/section/div[2]/div[1]/div/div/div/div/div[1]/div/h4').inner_text()
    if status:
        return True
    return False




# ==========================
#           MAIN
# ==========================
if __name__ == "__main__":
    with sync_playwright() as p:
        user_agent, cookie_str = dataRead()
        domain = "claimtrx.com"

        browser, context, page = create_browser(
            user_agent= user_agent,
            cookie_str= cookie_str,
            domain= domain
        )
        getbalance()
        while True:
            page.goto("https://claimtrx.com/faucet", wait_until="domcontentloaded", timeout=60000)
            print(page.title())
            try:
                claim_status = faucet(context,page)
                if claim_status:
                    cooldown(4*60,f'{lblue}Wait for next claim ',f'{lgreen}Claiming...          ')
            except:
                print(f'{lred}|!| Claim Fail')
        input(f"{lblack}Press Enter to close...")
        browser.close()


