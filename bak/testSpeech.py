#-*-coding:utf-8-*-
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_loop = 100

path = "D://iflytek/stp/client/nw/chromedriver"
chrome_options = Options()

chrome_options.add_argument( "nwapp=D:\iflytek\stp\client\stp-page-client")
print("01 initial done")

#在功能模块出现的时候点击“演讲记录”
driver = webdriver.Chrome( executable_path=path, chrome_options=chrome_options)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div/div[2]/ul/li[2]/div'))
    )
    element.click()
    print("02 Open speech")
finally:
    time.sleep(10)

#选择本机演示ppt
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[3]/ul/li[1]/p').click()
time.sleep(5)
print("03 select local")

#选择ppt
driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[3]/div[1]/div[2]/div/ul/li[1]/span[1]').click()
time.sleep(5)
print("04 select PPT")

#选择ppt
driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[3]/div[2]/div/a[1]').click()
time.sleep(5)
print("05 click open")

#选择本地麦克风
driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/div[1]/form/ul/li[3]/label').click()
time.sleep(5)
print("06 click mic")

#在音频选择页点击“下一步”
driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/div[2]/div/a').click()
time.sleep(5)
print("07 click next")

#开始演讲
driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[1]/div[1]/div/div[1]/div/button[1]').click()
time.sleep(5)
print("08 begin speech")

count = 0
while (count < _loop):
    #清空字幕
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[2]/div/div[3]/a[1]').click()
    time.sleep(5)
    print("09 click clean")
    count = count + 1
    time.sleep(500)

#暂停演讲
driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[1]/div[1]/div/div[1]/div/button[1]/span').click()
time.sleep(10)
print("10 click pause")

#继续演讲
driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[1]/div[1]/div/div[1]/div/button[1]/span').click()
time.sleep(5)
print("11 click continue")