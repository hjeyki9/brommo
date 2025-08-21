import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless=new")  # nếu cần headless

driver = uc.Chrome(
    options=options,
    version_main=139  # thay 139 bằng version major của Chrome bạn (gõ chrome://version)
)

driver.get('https://surfearner.com/cpa')
input('Enter to close')


