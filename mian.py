from joblib import Parallel, delayed
import zipfile
from random import choice, uniform
import sys
import subprocess
from fake_headers import Headers
import undetected_chromedriver as uc
import warnings
from plugin_config import *
import selenium
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
import indian_names
import random
from password_generator import PasswordGenerator
import requests
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import datetime, timedelta
import platform
from proxy_config import proxy
import traceback
import winsound


def notify_me():
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


def slow_type(element: WebElement, text: str, delay: float = 0.3):
    """Send a text to an element one character at a time with a delay."""
    for character in text:
        element.send_keys(character)
        time.sleep(uniform(.1, .3))


def URLGen(modelname, modelcode, size):
    # Generates URLs for releases on Adidas.com
    BaseSize = 580
    # Base Size is for Shoe Size 6.5
    ShoeSize = size - 6
    ShoeSize = ShoeSize * 20
    RawSize = ShoeSize + BaseSize
    ShoeSizeCode = int(RawSize)
    URL = 'https://www.adidas.co.in/' + str(modelname)+"/" +\
        str(modelcode) + '.html?forceSelSize=' + \
        str(modelcode) + '_' + str(ShoeSizeCode)
    return URL


def prepare_env():
    OSNAME = platform.system()

    if OSNAME == 'Linux':
        OSNAME = 'lin'
        with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()
    elif OSNAME == 'Darwin':
        OSNAME = 'mac'
        process = subprocess.Popen(
            ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode(
            'UTF-8').replace('Google Chrome', '').strip()
    elif OSNAME == 'Windows':
        OSNAME = 'win'
        process = subprocess.Popen(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )
        version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
    else:
        print('{} OS is not supported.'.format(OSNAME))
        sys.exit()

    major_version = version.split('.')[0]

    uc.TARGET_VERSION = major_version

    uc.install()

    return OSNAME


def prepare_proxy(proxy) -> webdriver.Chrome:

    OSNAME = prepare_env()

    proxy_split = proxy.split(":")
    PROXY_HOST = proxy_split[0]
    PROXY_PORT = proxy_split[1]
    PROXY_USER = proxy_split[2]
    PROXY_PASS = proxy_split[3]

    header = Headers(
        browser="chrome",
        os=OSNAME,
        headers=False
    ).generate()
    agent = header['User-Agent']

    options = webdriver.ChromeOptions()
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js %
                    (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS))
    options.add_extension(pluginfile)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    })
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-web-security")
    # viewport = ['2560,1440', '1920,1080']
    # options.add_argument(f"--window-size={choice(viewport)}")
    options.add_argument("--log-level=3")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f"user-agent={agent}")
    driver = webdriver.Chrome(options=options)

    return driver


def login_google_profile(wait: webdriver.Chrome, username, password):
    sign_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         "/html/body/div[1]/div[1]/div/div/div/div[2]/a")))
    sign_button.click()

    username_field = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")))
    slow_type(username_field, username)

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")))
    next_button.click()

    password_field = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")))
    slow_type(password_field, password)

    next_button2 = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")))
    next_button2.click()

    time.sleep(4)


def check_pincode(driver: webdriver.Chrome, wait: webdriver.Chrome, pincode):

    pincode_field = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                           "//input[@id='pincodeInputId']")))
    pincode_field.send_keys(pincode)

    check_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                          "//span[text()='Check']")))
    check_button.click()
    # time.sleep(2)


def add_to_bag(driver: webdriver.Chrome, wait: webdriver.Chrome, pincode):
    try:
        wait2 = WebDriverWait(driver, 1)
        check_pincode(driver=driver, wait=wait2, pincode=pincode)
    except:
        pass

    try:
        try:
            buy_now_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='BUY NOW' or text()='SHOP' or text()='BUY']")))
            buy_now_button.click()

        except:
            preorder_button = driver.find_element(
                By.XPATH, "//button[text()='PREORDER NOW' or text()='PREORDER']")
            preorder_button.click()
    except:
        wait = WebDriverWait(driver, 1)
        driver.refresh()
        add_to_bag(driver=driver, wait=wait, pincode=pincode)


def select_credit_card(driver: webdriver.Chrome, wait: webdriver.Chrome, cardnumber, cvv, exp_month, exp_year):

    credit_card = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                         "//label[@for='CREDIT']")))
    credit_card.click()
    print("Entering card details")

    notify_me()

    wait = WebDriverWait(driver, 30)

    card_field = wait.until(EC.element_to_be_clickable((By.NAME,
                                                        "cardNumber")))
    card_field.send_keys(cardnumber)

    cvv_field = wait.until(EC.element_to_be_clickable((By.NAME,
                                                       "cvv")))
    cvv_field.send_keys(cvv)

    month = Select(wait.until(
        EC.element_to_be_clickable((By.NAME, "month"))))
    month.select_by_value(exp_month)

    year = Select(wait.until(
        EC.element_to_be_clickable((By.NAME, "year"))))
    year.select_by_value(exp_year)


def main(_proxy, username, password, cardnumber, cvv, exp_month, exp_year, pincode):
    url = "https://www.flipkart.com/realme-9i-prism-black-64-gb/p/itm3e9987219f652?pid=MOBG9VGVYG2XHZGR&lid=LSTMOBG9VGVYG2XHZGRYBJYA7&marketplace=FLIPKART&store=tyy%2F4io&srno=b_1_2&otracker=clp_metro_expandable_1_3.metroExpandable.METRO_EXPANDABLE_Shop%2BNow_mobile-phones-store_Q1PDG4YW86MF_wp3&fm=neo%2Fmerchandising&iid=a19fc75a-8d64-4f94-8605-4ebb3bf1a65a.MOBG9VGVYG2XHZGR.SEARCH&ppt=clp&ppn=mobile-phones-store&ssid=50clk9mz340000001648097198467"
    url = r"https://www.flipkart.com/sony-playstation-5-cfi-1008a01r-825-gb-astro-s-playroom/p/itma0201bdea62fa?pid=GMCFYTWS68SAKTVV&lid=LSTGMCFYTWS68SAKTVVHXNXQO&marketplace=FLIPKART&q=ps5+game&store=4rr%2Fx1m&spotlightTagId=BestsellerId_4rr%2Fx1m&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&fm=search-autosuggest&iid=71dbb129-fb8f-4199-ba51-ca77cda4e81d.GMCFYTWS68SAKTVV.SEARCH&ppt=sp&ppn=sp&ssid=cx3x7npbao0000001648097145087&qH=04b3a1b04dc6441f"

    driver = prepare_proxy(_proxy)
    wait = WebDriverWait(driver, 10)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    print('\033[92m' + f'Proxy: {_proxy}' + '\033[0m')

    driver.get(url)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                          "/html/body/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div/div/a")))
    login_button.click()

    username_field = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                            "/html/body/div[3]/div/div/div/div/div[2]/div/form/div[1]/input")))
    username_field.send_keys(username)

    password_field = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                            "/html/body/div[3]/div/div/div/div/div[2]/div/form/div[2]/input")))
    password_field.send_keys(password)

    login_button2 = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                          "/html/body/div[3]/div/div/div/div/div[2]/div/form/div[4]/button")))
    login_button2.click()

    time.sleep(3)

    add_to_bag(driver=driver, wait=wait, pincode=pincode)

    continue_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'CONTINUE')]")))
    continue_button.click()

    select_credit_card(driver=driver, wait=wait, cardnumber=cardnumber,
                       cvv=cvv, exp_month=exp_month, exp_year=exp_year)

    continue_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'PAY')]")))
    continue_button.click()
    print("Enter otp on the screen")
    time.sleep(600)


if __name__ == "__main__":
    # _proxy = "103.199.187.217:45785:Selsharmashubham859:F4s1LzV"
    pincode = '121004'
    cardnumber = "4035620093318018"
    cvv = "732"
    exp_month = "01"
    exp_year = "29"
    username = "sharma.shubham859@gmail.com"
    password = "Shubhang07#"
    _proxy = "103.199.185.216:45785:Selsharmashubham859:F4s1LzV"
    main(_proxy, username=username, password=password,
         cardnumber=cardnumber, cvv=cvv, exp_month=exp_month, exp_year=exp_year, pincode=pincode)
