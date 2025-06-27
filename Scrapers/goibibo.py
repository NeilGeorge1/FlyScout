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
   
#############################################################     

from_city = sys.argv[1]
to_city = sys.argv[2]
date = sys.argv[3]

options = uc.ChromeOptions()
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

url = 'https://www.goibibo.com'
driver.get(url)

driver.implicitly_wait(5)

ActionChains(driver).move_by_offset(10, 10).click().perform()

closePopups(driver)

from_click_area = driver.find_element(By.XPATH, "//div[contains(@class, 'fswFld') and .//span[text()='From']]")
from_click_area.click()
from_input = driver.find_element(By.XPATH, "//div[contains(@class, 'fbAAhv')]//input[@type='text']")
from_input.clear()
from_input.send_keys(from_city)
time.sleep(1)
ActionChains(driver).send_keys(Keys.ENTER).perform()

to_input = driver.find_element(By.XPATH, "//div[.//span[text()='To']]/input")
to_input.click()
to_input.clear()
to_input.send_keys(to_city)
time.sleep(1)
ActionChains(driver).send_keys(Keys.ENTER).perform()

escape(driver)

departure_field = driver.find_element(By.XPATH, "//div[contains(@class, 'fswFld') and .//span[text()='Departure']]")
departure_field.click()
#target_date = "Wed Jun 25 2025"
desired_date = driver.find_element(By.XPATH, f"//div[@aria-label='{date}']")
desired_date.click()

escape(driver)

search_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'cJDpIZ') and .//span[text()='SEARCH FLIGHTS']]")
search_btn.click()

closePopups(driver)

try:
    flights = driver.find_elements(By.XPATH, "//div[@data-test='component-clusterItem']")
    
    if not flights:
        print("No flights found")

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

        # Print Output
        print("Cheapest Rates from Goibibo:")
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
        print("="*60)
        break  # Only the first flight (cheapest)
        
except Exception as e:
    print("Flights not found due to:", e)


time.sleep(1)
driver.quit()
