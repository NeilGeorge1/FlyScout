import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def escape(driver):
    try:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    except:
        pass

def closePopups(driver):
    popup_css = [".close", ".mfp-close"]
    for sel in popup_css:
        try:
            e = driver.find_element(By.CSS_SELECTOR, sel)
            driver.execute_script("arguments[0].click();", e)
        except:
            pass
    escape(driver)

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options, use_subprocess=True)
driver.get("https://www.cleartrip.com/")
driver.implicitly_wait(1)
ActionChains(driver).move_by_offset(10,10).click().perform()
closePopups(driver)

f = driver.find_element(By.XPATH, "//input[@placeholder='Where from?']")
f.click()
f.send_keys("Bengaluru")
time.sleep(1)

from_suggestion = driver.find_element(By.XPATH, "//li//p[contains(text(), 'Bengaluru')]")
from_suggestion.click()

ActionChains(driver).move_by_offset(100, 100).click().perform()

t = driver.find_element(By.XPATH, "//input[@placeholder='Where to?']")
t.click()
t.send_keys("Tokyo")
time.sleep(1)

to_suggestion = driver.find_element(By.XPATH, "//li//p[contains(text(), 'Tokyo')]")
to_suggestion.click()

ActionChains(driver).move_by_offset(100, 100).click().perform()


date_str = "Wed, Jun 25"  # or dynamically generated
xpath = f"//div[contains(@class, 'card-price') and text()='{date_str}']"
element = driver.find_element(By.XPATH, xpath)
element.click()
ActionChains(driver).move_by_offset(100, 100).click().perform()

closePopups(driver)

button = driver.find_element(By.XPATH, "//button[contains(@class, 'flex-1')]//h4[text()='Search flights']")
button.click()

time.sleep(2)
try:
    elem = driver.find_element(By.CSS_SELECTOR, "p.blackText.fontSize12[data-test='component-clusterHeader']")
    text = elem.text 
    price, duration = map(str.strip, text.split('|'))
    print("Price:", price)
    print("Duration:", duration)
except:
    print("Flights not found")
    
driver.quit()