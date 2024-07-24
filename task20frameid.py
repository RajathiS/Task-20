from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()


driver.get('https://www.cowin.gov.in/')
driver.maximize_window()

time.sleep(5)

faq_xpath = '//a[contains(text(), "FAQ")]'
partners_xpath = '//a[contains(text(), "Partners")]'

faq_element = driver.find_element(By.XPATH, faq_xpath)
faq_element.click()


partners_element = driver.find_element(By.XPATH, partners_xpath)
partners_element.click()


time.sleep(3)


windows = driver.window_handles


for window in windows:
    driver.switch_to.window(window)
    print(f"Window Title: {driver.title}, Frame ID: {window}")


main_window = driver.window_handles[0]
for window in windows:
    if window != main_window:
        driver.switch_to.window(window)
        driver.close()


driver.switch_to.window(main_window)


print(f"Current Window Title: {driver.title}")


driver.quit()
