__author__ = "jialin2"

import subprocess
import time
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from simulate_actions import actions4realtime


path = "D://iflytek/stp/client/nw/chromedriver"
chrome_options = Options()

chrome_options.add_argument("nwapp=D:\iflytek\stp\client\stp-page-client")
print("01 initial done")

# 启动telegraf
cmd = "d: && cd telegraf-1.10.1 && start.bat"
subprocess.Popen(cmd, shell=True)
print("02 run telegraf")

# 运行转写机客户端，检查页面元素（讲话速记模块入口）是否存在
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="module-button real-time-button"]'))
    )
except NameError:
    print("Exception happened")
    driver.quit()
else:
    print("03 open software")

    # 点击进入讲话速记模块
    driver.find_element_by_xpath('//div[@class="module-button real-time-button"]').click()
    time.sleep(2)
    print("04 open real-time")

    # 在音频选择页面选中内置麦克风
    driver.find_element_by_xpath('//input[@id="recordLocal"]').click()
    time.sleep(2)
    print("05 select local-mic")

    # 点击下一步
    driver.find_element_by_xpath('//*[@class="record-select-confirm-action"]').click()
    time.sleep(2)
    print("06 click next")

    # 点击开始按钮，开始速记，打印开始时间
    driver.find_element_by_xpath('//div[@class="realtime-trans-start-action"]').click()
    print("07 begin record, start time is " + time.asctime(time.localtime(time.time())))

    print("08 start executing actions")
    num = 1
    while True:
        timer = threading.Timer(10, actions4realtime, (driver, num,))
        timer.start()
        time.sleep(60)
        # 获取速记持续时间的小时数
        duration = driver.find_element_by_class_name('realtime-trans-timer').get_attribute('textContent')
        hours = int(duration[3:5])
        print(str(hours) + "minute(s) past")
        # 大于指定时长(10 hours)后跳出循环
        if hours > 10:
            print("10 stop executing actions, current time is " + time.asctime(time.localtime(time.time())))
            break
        else:
            num += 1
