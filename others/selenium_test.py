from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
import time
s = Service('/usr/local/bin/chromedriver')
browser = webdriver.Chrome(service=s)
browser.implicitly_wait(10)
browser.get("https://vmid-uat.vfcorp.com.cn/login")
time.sleep(3)
# browser.find_element(By.XPATH, '//*[@id="login-form"]')
# browser.switch_to.frame(browser.find_element(By.ID, ""))
browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/input').send_keys("metersphere")
browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/input').send_keys("metersphere")
draggable = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[3]')
start = draggable.location
print(start['x'],'~~', start['y'])
ActionChains(browser).drag_and_drop_by_offset(draggable, 400, 0).perform()
browser.find_element(By.XPATH, '//*[@id="btn"]').click()
browser.quit()