import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


download_dir = os.path.join(os.getcwd(), "PhotoGallery")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)


chrome_options = Options()
chrome_options.add_argument("--incognito")  
chrome_options.add_experimental_option("prefs", {
    "plugins.always_open_pdf_externally": True,
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,  
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


driver.get("https://labour.gov.in/")


try:
    
    media_menu = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Media']"))
    )
   
    media_menu.click()
    
    more_info = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Click for more info of Press Releases']"))
    )
    more_info.click()


    photo = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "(//a[normalize-space()='Photo Gallery'])[2]"))
    )
    href = photo.get_attribute('href')
   
    driver.get(href)
    time.sleep(5)
    window_after = driver.window_handles[0]
    image_elements = driver.find_elements(By.XPATH, "//table//img")
    time.sleep(2)
 
    image_urls = [element.get_attribute('src') for element in image_elements[:10]]
 
    for i, url in enumerate(image_urls, 1):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(download_dir, f"image_{i}.jpg"), "wb") as f:
                    f.write(response.content)
                    print(f"Downloaded image {i}")
            else:
                print(f"Failed to download image {i}")
        except Exception as e:
            print(f"Error occurred while downloading image {i}: {str(e)}")


except Exception as e:
    print(f"An error occurred: {str(e)}")


finally:
    
    driver.quit()
