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

#在功能模块出现的时候点击“讲话速记”
driver = webdriver.Chrome( executable_path=path, chrome_options=chrome_options)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div/div[2]/ul/li[1]/div'))
    )
    element.click()
    print("02 Open real-time")
finally:
    time.sleep(10)

#在音频选择页选择本地内置麦克风
driver.find_element_by_xpath('/html/body/div[8]/div/div/div/div[2]/div[1]/form/ul/li[3]/label').click()
time.sleep(5)
print("03 select mic")

#在音频选择页点击“下一步”
driver.find_element_by_xpath('/html/body/div[8]/div/div/div/div[2]/div[2]/div/a').click()
time.sleep(5)
print("04 click next")

#开始速记
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]').click()
time.sleep(5)
print("05 begin record")

count = 0
while (count < _loop):
    #编辑区域获取焦点，输入hello...
    element01 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[3]/div/div[1]')
    element01.click()
    time.sleep(50)
    print("06 get focus")
    element01.send_keys("hello,we will input something in the editor")
    time.sleep(5)
    print("07 input hello...")

    #暂停速记
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[1]/div[3]').click()
    time.sleep(10)
    print("08 pause")

    #编辑区域获取焦点，输入你好...
    element02 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[3]/div/div[1]')
    element02.click()
    time.sleep(10)
    print("09 get focus")
    element02.send_keys(u'哈哈哈哈哈哈！！！你好，我会在编辑器中添加一些汉字！！！哈哈哈哈哈')
    time.sleep(5)
    print(u'10 input 你好...')
    
    #继续速记
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]').click()
    time.sleep(10)
    print("11 continue")
    
    time.sleep(500)
    count = count + 1

#点击查找替换
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[1]/ul/li[1]/a').click()
time.sleep(10)
print("12 find&replace")

#替换"你"为"我"
element03 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div/input')
element03.click()
time.sleep(5)
print("13 find content")
element03.send_keys(u'你')

element04 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/input')
element04.click()
time.sleep(5)
print("14 replace content")
element04.send_keys(u'我')

#点击替换
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/a[1]').click()
time.sleep(10)
print("15 replace")

#点击X关闭查找替换栏
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/a').click()
time.sleep(10)
print("16 find&replace")

#点击查找替换
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[1]/ul/li[1]/a').click()
time.sleep(10)
print("17 find&replace")

#替换"我"为"你"
element05 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div/input')
element05.click()
time.sleep(5)
print("18 find content")
element05.send_keys(u'我')

element06 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/input')
element06.click()
time.sleep(5)
print("19 replace content")
element06.send_keys(u'你')

#点击全部替换
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/a[2]').click()
time.sleep(10)
print("20 replace ALL")




