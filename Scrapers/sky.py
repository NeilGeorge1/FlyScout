import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re

def escape(driver):
    try:
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ESCAPE)
    except:
        print("Escape Key didn’t work!")

def closePopups(driver):
    popup_selectors = [
        ".commonModal__close",
        ".langCardClose",
        ".overlayCrossIcon",
        ".newsletter__close",
        "#webklipper-publisher-widget-container .close",
    ]
    for selector in popup_selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script("arguments[0].click();", element)
            print(f"Closed popup: {selector}")
        except:
            pass
    try:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    except:
        print("Could not send ESCAPE")
    try:
        got_it_btn = driver.find_element(By.CSS_SELECTOR, "span[data-testid='coachmark-overlay-button']")
        if got_it_btn.is_displayed():
            got_it_btn.click()
            print("Closed: GOT IT coachmark popup")
    except:
        print("Could not close the GOT IT")

def increase_count(driver, label, target_count):
    section = driver.find_element(By.XPATH, f"//p[text()='{label}']/ancestor::div[contains(@class, 'pZQPB')]")
    count_elem = section.find_element(By.XPATH, ".//span[contains(@class, 'jueHCN')]")
    plus_btn = section.find_elements(By.XPATH, ".//span[contains(@class, 'kZvHQU')]")[1]
    current = int(count_elem.text)
    while current < target_count:
        plus_btn.click()
        time.sleep(0.2)
        current += 1

def scrape_flights(title_text):
    try:
        flights = driver.find_elements(By.XPATH, "//div[@data-test='component-clusterItem']")
        if not flights:
            print(f"No flights found for {title_text}")
            return
        print(f"\n{title_text} Flights from Goibibo:\n")
        count = 0
        for flight in flights:
            airline = flight.find_element(By.XPATH, ".//p[@data-test='component-airlineHeading']").text
            flight_code = flight.find_element(By.CLASS_NAME, "fliCode").text
            departure_time = flight.find_element(By.XPATH, ".//div[contains(@class,'timeInfoLeft')]//span").text
            departure_city = flight.find_element(By.XPATH, ".//div[contains(@class,'timeInfoLeft')]//font").text
            arrival_time = flight.find_element(By.XPATH, ".//div[contains(@class,'timeInfoRight')]//span[1]").text
            try:
                arrival_day = flight.find_element(By.XPATH, ".//div[contains(@class,'timeInfoRight')]//span[contains(text(),'+')]").text
            except:
                arrival_day = ""
            arrival_info = flight.find_element(By.XPATH, ".//div[contains(@class,'timeInfoRight')]//font").text
            duration = flight.find_element(By.XPATH, ".//div[contains(@class, 'stop-info')]//p[1]").text
            stops = flight.find_element(By.XPATH, ".//p[contains(@class,'flightsLayoverInfo')]").text
            price = flight.find_element(By.XPATH, ".//div[contains(@class,'clusterViewPrice')]//span").text
            try:
                lock_price = flight.find_element(By.XPATH, ".//span[@data-test='component-lockPricePersuasionText']").text
            except:
                lock_price = "N/A"
            try:
                discount_info = flight.find_element(By.XPATH, ".//p[contains(@class,'alertMsg')]").text
            except:
                discount_info = "N/A"
            try:
                refund_policy = flight.find_element(By.XPATH, ".//span[contains(@class,'ftr-persuasion')]").text
            except:
                refund_policy = "N/A"
            try:
                logo_element = flight.find_element(By.XPATH, ".//span[contains(@class, 'arln-logo')]")
                style_attr = logo_element.get_attribute("style")
                match = re.search(r'url\(&quot;(.+?)&quot;\)', style_attr)
                logo_url = match.group(1) if match else ""
            except:
                logo_url = ""
            try:
                link_element = flight.find_element(By.XPATH, ".//a[contains(@class, 'FlightListingCard')]")
                goibibo_link = link_element.get_attribute("href")
            except:
                goibibo_link = url
            print("Airline:", airline)
            print("Flight Code(s):", flight_code)
            print("Departure:", f"{departure_time} — {departure_city}")
            print("Arrival:", f"{arrival_time} {arrival_day} — {arrival_info}")
            print("Duration:", duration)
            print("Stops:", stops)
            print("Price:", price)
            print("Lock Price Info:", lock_price)
            print("Discount Offers:", discount_info)
            print("Refund Policy:", refund_policy)
            print("Logo URL:", logo_url)
            print("Goibibo Link:", goibibo_link)
            print("---")
            count += 1
            if count >= 3:
                break
    except Exception as e:
        print(f"Flights not found due to: {e}")

# ========== SCRIPT START ==========

"""from_city = sys.argv[1]
to_city = sys.argv[2]
date = sys.argv[3]
adults = int(sys.argv[4])
children = int(sys.argv[5])
infants = int(sys.argv[6])  
travelClass = sys.argv[7]"""

options = uc.ChromeOptions()
#options.add_argument("--headless=new")
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

prefs = {
    "profile.default_content_setting_values.notifications": 2
}
options.add_experimental_option("prefs", prefs)

driver = uc.Chrome(options=options, use_subprocess=True)

url = 'https://www.kayak.com'
driver.get(url)
driver.implicitly_wait(1)
ActionChains(driver).move_by_offset(10, 10).click().perform()
actions = ActionChains(driver)

closePopups(driver)

from_input = driver.find_element(By.XPATH, "//input[@aria-label='Flight origin input']")
from_input.click()
from_input.clear()
from_input.send_keys("Bengaluru")
time.sleep(2)  # wait for suggestions to appear
actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
time.sleep(1)

to_input = driver.find_element(By.XPATH, "//input[@aria-label='Flight destination input']")
to_input.click()
to_input.clear()
to_input.send_keys("Tokyo")
time.sleep(2)  # wait for suggestions to appear
actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
time.sleep(1)

# Departure date
departure_card = driver.find_element(By.XPATH, "//div[@aria-label='Departure date']")
departure_card.click()
time.sleep(1)
date_button = driver.find_element(By.XPATH, "//button[normalize-space()='1']")
date_button.click()

escape(driver)

# ✅ Travellers & Class selection
info_click = driver.find_element(By.XPATH, "//div[contains(@class, 'fswFld') and .//span[text()='Travellers & Class']]")
info_click.click()
time.sleep(1)
increase_count(driver, "Adults", adults)
increase_count(driver, "Children", children)
increase_count(driver, "Infants", infants)
travel_class = travelClass
class_xpath = f"//li[text()='{travel_class.lower()}']"
driver.find_element(By.XPATH, class_xpath).click()

try:
    done_button = driver.find_element(By.XPATH, "//a[contains(@class, 'sc-12foipm-64') and contains(text(), 'Done')]")
    if done_button.is_displayed():
        driver.execute_script("arguments[0].click();", done_button)
        print("✅ Clicked 'Done' to apply Travellers & Class changes")
    else:
        print("❌ 'Done' button not visible")
except Exception as e:
    print(f"❌ Failed to click 'Done': {e}")

escape(driver)

# 🔍 Click search
search_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'cJDpIZ') and .//span[text()='SEARCH FLIGHTS']]")
search_btn.click()

closePopups(driver)

# ✈ Scrape flights
scrape_flights("Cheapest")
time.sleep(1)

cluster_tabs = driver.find_elements(By.XPATH, "//div[@data-test='component-clusterTabItem']")
if len(cluster_tabs) > 1:
    cluster_tabs[1].click()
    scrape_flights("Second Tab (Fastest/Non Stop)")
else:
    print("Second tab not found.")

time.sleep(1)
driver.quit()
