#-*-coding:utf-8-*-
__author__ = "xuma@iflytek.com"

import os
import time
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

_loop = 100

path = "D://iflytek/stp/client/nw/chromedriver"
chrome_options = Options()

chrome_options.add_argument( "nwapp=D:\iflytek\stp\client\stp-page-client")
print("01 initial done")

# 启动telegraf
cmd = "d: && cd telegraf-1.10.1 && start.bat"
subprocess.Popen(cmd, shell=True)
print("02 run telegraf")

# 输入希望运行的时长
time.sleep(2)
t = int(input("please enter the hours you wish the script lasts: "))

# 在功能模块出现的时候点击“讲话速记”
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div/div[2]/ul/li[1]/div'))
    )
    element.click()
    print("03 Open real-time")
finally:
    time.sleep(10)

# 在音频选择页选择本地内置麦克风
driver.find_element_by_xpath('/html/body/div[8]/div/div/div/div[2]/div[1]/form/ul/li[3]/label').click()
time.sleep(5)
print("04 select mic")

# 在音频选择页点击“下一步”
driver.find_element_by_xpath('/html/body/div[8]/div/div/div/div[2]/div[2]/div/a').click()
time.sleep(5)
print("05 click next")

# 开始速记
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]').click()
time.sleep(5)
print("06 begin record")

while True:
    # 执行js使讲话人列表及字幕区滚动到最底部
    """
    首先获取讲话人列表对象el，整个编辑区对象el1，
    判断讲话人列表高度是否大于编辑区对象固定显示高度824，若大于则表示内容已超出一屏，
    此时设置el1被卷去的高度scrollTop为内容高度与固定显示高度只差
    """
    js = 'var el = document.getElementsByClassName("hisee-speaker-list-wrap")[0];' \
         'var el1 = document.getElementsByClassName("zxzd-editor-wrap")[0];' \
         'if (el.scrollHeight - 824 > 0) {el1.scrollTop = el.scrollHeight - 824};'
    driver.execute_script(js)
    time.sleep(60)

    # 编辑区域获取焦点，输入hello...
    '''
    element01 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[3]/div/div[1]')
    element01.click()
    '''
    # 将鼠标定位到字幕区第一行文本的起始位置
    ActionChains(driver).move_by_offset(445, 299).click().perform()
    print("07 get focus on the beginning of first paragraph")
    time.sleep(1)
    zxzd = driver.find_element_by_xpath('//div[@class="hisee-editor zxzd-editor"]')
    zxzd.send_keys("hello,we will input something in the editor")
    # element01.send_keys("hello,we will input something in the editor")
    print("08 input hello...")
    time.sleep(10)

    # 暂停速记
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[1]/div[3]').click()
    time.sleep(2)
    print("09 pause")

    # 编辑区域获取焦点，输入你好...
    '''
    element02 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[3]/div/div[1]')
    element02.click()
    '''
    ActionChains(driver).move_by_offset(0, 0).perform()
    ActionChains(driver).move_by_offset(445, 299).click().perform()
    print("10 get focus")
    time.sleep(1)
    zxzd.send_keys(u'哈哈哈哈哈哈！！！你好，我会在编辑器中添加一些汉字！！！哈哈哈哈哈')
    time.sleep(5)
    print(u'10 input 你好...')

    ActionChains(driver).move_by_offset(0, 0).perform()
    driver.execute_script(js)
    time.sleep(1)

    # 继续速记
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[1]/div[2]').click()
    time.sleep(10)
    print("11 continue")

    time.sleep(20)
    # 获取讲话速记已持续的小时数
    duration = driver.find_element_by_class_name('realtime-trans-timer').get_attribute('textContent')
    hours = int(duration[:2])
    print(str(hours) + "hour(s) past")
    # 大于用户指定时长后跳出循环
    if hours == t:
        print("Jump out the circle, current time is " + time.asctime(time.localtime(time.time())))
        break

# 点击查找替换
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[1]/ul/li[1]/a').click()
time.sleep(5)
print("12 find&replace")

# 替换"你"为"我"
element03 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div/input')
element03.click()
time.sleep(2)
print("13 find content")
element03.send_keys(u'你')

element04 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/input')
element04.click()
time.sleep(2)
print("14 replace content")
element04.send_keys(u'我')

# 点击替换
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/a[1]').click()
time.sleep(5)
print("15 replace")

# 点击X关闭查找替换栏
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/a').click()
time.sleep(10)
print("16 find&replace")

# 点击查找替换
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[1]/ul/li[1]/a').click()
time.sleep(5)
print("17 find&replace")

# 替换"我"为"你"
element05 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div/input')
element05.click()
time.sleep(2)
print("18 find content")
element05.send_keys(u'我')

element06 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/input')
element06.click()
time.sleep(2)
print("19 replace content")
element06.send_keys(u'你')

# 点击全部替换
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/a[2]').click()
time.sleep(5)
print("20 replace ALL")

# 点击X关闭查找替换栏
driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[2]/div/a').click()
time.sleep(10)
print("21 find&replace")

# 恢复自动滚动
driver.execute_script(js)

print("22 End the conference")
driver.find_element_by_class_name('realtime-trans-end-action').click()

