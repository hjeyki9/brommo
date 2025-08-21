# -*- coding: utf-8 -*-
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import pygetwindow as gw
import time, os, requests, sys, itertools, pyautogui
from bs4 import BeautifulSoup
from colorama import Style, Fore, init

init(autoreset=True)

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

def delete_link(linkdel):
    with open("videos.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open("videos.txt", "w", encoding="utf-8") as f:
        for line in lines:
            if not line.startswith(linkdel):
                f.write(line)
#COLOR
def create_color():
    global lgreen,lblue,green,yellow,lyellow,grey,lred,red,white,purple,pink,aqua,cyan,blue,bold,reset
    lgreen = Fore.LIGHTGREEN_EX
    lblue = Fore.LIGHTBLUE_EX
    green = Fore.GREEN
    yellow = Fore.YELLOW
    lyellow = Fore.LIGHTYELLOW_EX
    grey = Fore.LIGHTBLACK_EX
    lred = Fore.LIGHTRED_EX
    red = Fore.RED
    white = Fore.WHITE
    purple = Fore.MAGENTA
    pink = Fore.LIGHTMAGENTA_EX
    aqua = Fore.LIGHTCYAN_EX
    cyan = Fore.CYAN
    blue = Fore.BLUE
    bold = Style.BRIGHT
    reset = Style.RESET_ALL

create_color()

def create_chrome_driver():
    options = uc.ChromeOptions()
    options.add_argument(f"--user-agent={user_agent}")

    # Ẩn automation flag
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Tắt tiếng
    options.add_argument("--mute-audio")

    # Tắt thông báo trình duyệt
    prefs = {
        "profile.default_content_setting_values.notifications": 2,  # chặn thông báo
        #"profile.default_content_setting_values.geolocation": 2,    # chặn định vị
        "profile.default_content_setting_values.media_stream_mic": 2,   # chặn mic
        "profile.default_content_setting_values.media_stream_camera": 2, # chặn camera
        "profile.default_content_setting_values.popups": 0          # chặn popup
    }
    options.add_experimental_option("prefs", prefs)

    # Tắt cảnh báo SSL, HTTPS
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return uc.Chrome(options=options)

def readData():
    try:
        with open('data.txt','r',encoding='utf-8') as f:
            user_agent = f.readline().strip()
            cookie_str = f.readline()
    except:
        user_agent = input('> Input User Agent: ')
        cookie_str = input('> Input Cookie: ')
        with open('data.txt','w',encoding='utf-8') as f:
            f.write(user_agent+'\n'+cookie_str)
    cookie_dict = dict( part.strip().split("=", 1) for part in cookie_str.split(";") if "=" in part)
    cookie_list = [{"name": k, "value": v} for k, v in cookie_dict.items()]
    cookies = dict(item.split("=", 1) for item in cookie_str.split("; "))
    return user_agent,cookie_list,cookies

def loadDataPage(page):
    headers = {
        'User-Agent': user_agent.strip(),
    }
    r = requests.get(f'https://rewardvid.com/?page={page}', headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = []
    times = []
    for div in soup.find_all("div", class_="video-post"):
        a_tag = div.find("a", href=True)
        if a_tag:
            links.append(a_tag["href"])
        time_span = div.find("span", class_="video-post-time")
        if time_span:
            times.append(time_span.get_text(strip=True))
    return links, times

def clear():
    os.system('cls')
user_agent, cookie_list, cookies = readData()
    
def banner():
    clear()
    print(f'{lred}----- REWARDVID.COM BOT AUTOMATION -----')
    print(f'{aqua} Copyright 2025 by BroMMO')
    
banner()
print('1.Start with current video data')
print('2.Start with load new video data')
choice = input()
if choice == '2':
    if os.path.exists('videos.txt'):
        os.remove('videos.txt')
    
# Create browser
driver = create_chrome_driver()
wait = WebDriverWait(driver, 10)  # tối đa 10 giây
actions = ActionChains(driver)

driver.get('https://rewardvid.com/')
for c in cookie_list:
    driver.add_cookie(c)
driver.refresh()
print(Fore.LIGHTGREEN_EX+'Login succesful')
print(Fore.LIGHTRED_EX+"If bot can't login, please delete data.txt file then try again!")
print(Fore.RED+'When the tool running, please keep chrome full size')
link_list = []
time_list = []
earn = 0
watch = 0
time.sleep(5)
while True:
    try:
        with open('videos.txt','r',encoding='utf-8') as f:
            data = [line.strip().split("|") for line in f]
        print(f'{lgreen}Loading videos data from videos.txt')
        link_list = [item[0] for item in data]
        time_list = [item[1] for item in data]
        print(f'{lgreen}Now, Bot will use video list from videos.txt , If you want to use new data, please delete videos.txt file!')
    except FileNotFoundError:
        print(f'{lgreen}Trying get full video datas from rewardvid.com')
        for i in range(1,7):
            links, times = loadDataPage(i)
            link_list.extend(links)
            time_list.extend(times)
        with open("videos.txt", "a", encoding="utf-8") as f:
            for a, b in zip(link_list, time_list):
                f.write(f"{a}|{b}\n")
        print(f'{lgreen}Success get full video datas from rewardvid.com')

    for i in range(len(link_list)):
        try:
            print(f'{lgreen}Opening new video: {white}{link_list[i]}')
            print(f'{lyellow}Video watch time: {white}{time_list[i]}')
            driver.get(link_list[i])
            time.sleep(3)
            try:
                please_wait=driver.find_element(By.XPATH,'/html/body/div[3]/section/div/div/div[1]/div[1]/h6').text
                if please_wait == 'Wait for the Timer to Finish to Watch this Video Again':
                    print(f'{lred}This video has been watched before!')
                    continue
            except:
                pass
            rewardtext = driver.find_element(By.XPATH,'/html/body/div[3]/section/div/div/div[2]/div[4]/div/div[1]').text
            balance = driver.find_element(By.XPATH,'/html/body/div[3]/header/nav/div/div[3]/div[4]/a[2]').text
            pooltext = driver.find_element(By.XPATH,'/html/body/div[3]/section/div/div/div[2]/div[3]/h1').text
            reward = ""
            for test in rewardtext:
                if test.isdigit() or test==".":
                    reward+= test
            reward = float(reward)
            pool = ''
            for test in pooltext:
                if test.isdigit() or (test in '.'):
                    pool += test
            pool = float(pool)
            if pool < reward*2:
                print(f'{lred}This video has no reward money, the bot will ignore it')
                delete_link(link_list[i])
                continue
            print('Trying click to play video')
            #body = driver.find_element("tag name", "body")
            #size = body.size
            #x = min(400, size['width'] - 5)
            #y = min(400, size['height'] - 5)
            #print('Found body')
            #actions.move_to_element_with_offset(body, 0, 0).perform()
            #print('Moved the mouse')
            #actions.move_by_offset(x, y).click().perform()
            title = driver.title
            window = gw.getWindowsWithTitle(title)
            if window:
                for test in range(3):
                    time.sleep(0.2)
                    window[0].activate()
                    time.sleep(0.2)
            time.sleep(0.5)
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            pyautogui.click(center_x, center_y)
            time.sleep(0.1)
            try:
                tabs = driver.window_handles
                driver.switch_to.window(tabs[1])
                driver.close()
                driver.switch_to.window(tabs[0])
                time.sleep(0.5)
                pyautogui.click(center_x, center_y)
            except:
                pass
            view_time_str = time_list[i]
            view_time = int(view_time_str[0]+view_time_str[1])*60*60+int(view_time_str[3]+view_time_str[4])*60+int(view_time_str[6]+view_time_str[7])
            time.sleep(1)
            cooldown(view_time,f'{aqua}Video Remaining: ',f'{lgreen}Video has been watched!              ')
            #cooldown(1,f'{lyellow}Video Remaining: ',f'{lgreen}Video has been watched!              ')
            print(f'{lgreen}Earned: {reward}$')
            earn += reward
            watch += 1
            print(f'{white}$Balance: {lyellow}{lgreen}{balance}{white} | Total watched: {aqua}{watch}{white} | Total earned: {lgreen}{earn:.3f}$')
            delete_link(link_list[i])
            time.sleep(2)
        except:
            print(f"{lred}[X] Can't watch video!")
            delete_link(link_list[i])
            time.sleep(2)
    os.remove('videos.txt')

print(f'{lgreen}DONE!!')
input('Enter to close')
driver.quit()

