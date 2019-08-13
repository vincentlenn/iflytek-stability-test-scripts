# -*-coding:utf-8-*-
__author__ = "jialin2@iflytek.com"

import subprocess
import time
import datetime
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from simulate_actions import actions4DVRmode


path = "D://iflytek/stp/client/nw/chromedriver"
chrome_options = Options()

chrome_options.add_argument("nwapp=D:\iflytek\stp\client\stp-page-client")
print("01 initial done")

# 启动telegraf
cmd = "d: && cd telegraf-1.10.1 && start.bat"
subprocess.Popen(cmd, shell=True)
print("02 run telegraf")

'''
time.sleep(2)
t = int(input("please enter the running time(hours): "))
'''

# 运行转写机客户端，检查页面元素（字幕上屏模块入口）是否存在
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="module-button caption-subtitle-button"]'))
    )
except NameError:
    print("Exception happened")
    driver.quit()
else:
    print("03 open software")

    # 点击进入字幕上屏模块
    driver.find_element_by_xpath('//div[@class="module-button caption-subtitle-button"]').click()
    time.sleep(2)
    print("04 enter subtitle module")

    # 选择视频叠加字幕模式
    driver.find_element_by_xpath('//p[@class="caption-video-title"]').click()
    time.sleep(2)
    print("05 enter DVR subtitle")

    # 点击我已连接视频线
    driver.find_element_by_xpath('//div[@class="dialog-actions"]').click()

    # 在音频选择页面选中视频内音频，点击下一步
    try:
        element = WebDriverWait(driver, 30, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="record-device-select-dialog-wrap"]'))
        )
    except BaseException:
        print("No signal")
        driver.quit()
    else:
        driver.find_element_by_xpath('//input[@id="recordDvr"]').click()
        time.sleep(2)
        ActionChains(driver).click(driver.find_element_by_xpath('//div[@class="record-info-wrap"]/a')).perform()
        print("07 select radio input")

        # 判断前端的会议控制窗口是否可见
        try:
            element = WebDriverWait(driver, 30, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="conference-control-panel-wrap"]'))
            )
        except BaseException:
            print("Control panel is invisible")
            driver.quit()
        else:
            time.sleep(10)
            # 判断字幕是否打开，若关闭则点击打开
            switch = driver.find_element_by_xpath('//div[@class="subtitle-switch"]/i')
            switch_status = switch.get_attribute('class')
            if switch_status == 'close':
                switch.click()

            # 自动适配字幕设置为默认
            adaption_btn = driver.find_element_by_xpath('//div[@class="subtitle-setting-attribute-frame"]/div[1]')
            if adaption_btn.get_attribute('class') == 'subtitle-adaption ':
                adaption_btn.click()

            time.sleep(2)
            # 点击开始按钮，开始字幕上屏，打印开始时间
            driver.find_element_by_xpath('//button[@class="control-item control-start"]').click()
            print("08 begin record, start time is " + time.asctime(time.localtime(time.time())))

            print("09 start executing actions")
            # 以下代码循环执行模拟用户操作
            n = 1
            while True:
                timer = threading.Timer(30, actions4DVRmode, (driver,))
                timer.start()
                time.sleep(120)
                # 获取演讲持续时间的小时数
                duration = driver.find_element_by_class_name('conference-time').get_attribute('textContent')
                hours = int(duration[:2])
                print(str(hours) + "hour(s) past")
                # 大于指定时长(10 hours)后跳出循环，且每小时暂停一次会议
                if hours > 10:
                    print("10 stop executing actions, current time is " + time.asctime(time.localtime(time.time())))
                    break
                elif hours == n:
                    n += 1
                    driver.find_element_by_xpath('//button[@class="control-item control-pause"]').click()
                    print("pause the speech")
                    time.sleep(10)
                    driver.find_element_by_xpath('//button[@class="control-item control-continue"]').click()
                    print("continue")

