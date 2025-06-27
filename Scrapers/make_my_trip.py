import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def escape(driver):
    try:
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ESCAPE)
    except:
        print("Escape Key didnt work!")

def closePopups(driver):
    popup_selectors = [
        ".commonModal__close",                # login popup
        ".langCardClose",                     # language/currency modal
        ".overlayCrossIcon",                  # offer banner overlay
        ".newsletter__close",                 # newsletter sign-up
        "#webklipper-publisher-widget-container .close",  # chatbot or feedback popups
    ]

    for selector in popup_selectors:
        try:
            element = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            driver.execute_script("arguments[0].click();", element)
            print(f"Closed popup: {selector}")
        except Exception:
            pass  

    try:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    except:
        print("Could not send ESCAPE")

from_city = sys.argv[1]
to_city = sys.argv[2]
date_str = sys.argv[3]

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options, use_subprocess=True)
driver.get("https://www.makemytrip.com")

driver.implicitly_wait(2)
ActionChains(driver).move_by_offset(10, 10).click().perform()

escape(driver)
closePopups(driver)

from_click_area = driver.find_element(By.XPATH, "//label[@for='fromCity']")
from_click_area.click()
from_input = driver.find_element(By.XPATH, "//input[@placeholder='From']")
from_input.send_keys(from_city)
time.sleep(1)
ActionChains(driver).move_by_offset(0, 100).click().perform()

escape(driver)
closePopups(driver)

to_click_area = driver.find_element(By.XPATH, "//label[@for='toCity']")
to_click_area.click()
to_input = driver.find_element(By.XPATH, "//input[@placeholder='To']")
to_input.send_keys(to_city)
time.sleep(1)
ActionChains(driver).move_by_offset(0, 100).click().perform()

escape(driver)
closePopups(driver)

departure_field = driver.find_element(By.XPATH, "//label[@for='departure']")
departure_field.click()
desired_date = driver.find_element(By.XPATH, f"//div[@aria-label='{date_str}']")
desired_date.click()

escape(driver)
closePopups(driver)

search_btn = driver.find_element(By.CSS_SELECTOR, "a.widgetSearchBtn")
search_btn.click()

escape(driver)
closePopups(driver)

time.sleep(1)

try:
    elem = driver.find_element(By.CSS_SELECTOR, "p.blackText.fontSize12[data-test='component-clusterHeader']")
    text = elem.text 
    price, duration = map(str.strip, text.split('|'))
    print("Price:", price)
    print("Duration:", duration)
except:
    print("Flights not found")

driver.quit()