#-*-coding:utf-8-*-
__author__ = "xuma@iflytek.com"

import subprocess
import time
import random

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

chrome_options.add_argument("nwapp=D:\iflytek\stp\client\stp-page-client")
print("01 initial done")

# 启动telegraf
cmd = "d: && cd telegraf-1.10.1 && start.bat"
subprocess.Popen(cmd, shell=True)
print("02 run telegraf")

# 在功能模块出现的时候点击“演讲记录”
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div/div[2]/ul/li[2]/div'))
    )
    element.click()
    print("03 Open speech")
finally:
    time.sleep(10)

    # 选择本机演示ppt
    driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[3]/ul/li[1]/p').click()
    time.sleep(5)
    print("04 select local")

    '''
    # 选择ppt文件（列表中第一个PPT文件，要求仅插入一个U盘且U盘内仅有一个PPT文件）
    driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[3]/div[1]/div[2]/div/ul/li[1]/span[1]').click()
    time.sleep(5)
    '''

    # 使用js选择指定PPT文件，但无法真正触发点击事件
    js = 'var li = document.getElementsByTagName("li");' \
         'for(var i = 0; i < li.length; ++i ){' \
         'if(li[i].getAttribute("title") == "1分钟自动翻页"){li[i].className = "choosed"; break;}};'
    driver.execute_script(js)
    # 模拟鼠标点击行为
    ActionChains(driver).move_to_element(driver.find_element_by_xpath('//li[@class="choosed"]')).click().perform()

    print("05 select PPT")
    time.sleep(2)

    # 点击打开
    driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[3]/div[2]/div/a[1]').click()
    time.sleep(5)
    print("06 click open")

    # 选择本地麦克风
    driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/div[1]/form/ul/li[3]/label').click()
    time.sleep(5)
    print("07 click mic")

    # 在音频选择页点击“下一步”
    driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/div[2]/div/a').click()
    time.sleep(5)
    print("08 click next")

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
        # print(switch_status)
        if switch_status == 'close':
            switch.click()

        time.sleep(2)
        # 开始演讲
        driver.find_element_by_xpath('//button[@class="control-item control-start"]').click()
        print("09 begin speech")

        # 自动适配字幕设置为默认
        adaption_btn = driver.find_element_by_xpath('//div[@class="subtitle-setting-attribute-frame"]/div[1]')
        print(adaption_btn.get_attribute('class'))
        if adaption_btn.get_attribute('class') == 'subtitle-adaption ':
            adaption_btn.click()
            print('adapt subtitle')
        time.sleep(30)
        count = 0
        while (count < _loop):
            # 在指定范围内生成随机坐标x,y, 预览窗口参数x: 100 y: 120 w: 1086 h: 611
            x = random.randint(100, 1186)
            y = random.randint(120, 731)
            subtitle = driver.find_element_by_class_name('subtitle-content-box')
            # 拖动预览字幕条到指定位置
            ActionChains(driver).drag_and_drop_by_offset(subtitle, x, y).perform()
            print("drag and drop the subtitle to %s, %s" % (x, y))
            time.sleep(10)

            # 清空字幕
            driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[2]/div/div[3]/a[1]').click()
            print("10 click clean")
            count = count + 1

            time.sleep(60)
            if adaption_btn.get_attribute('class') == 'subtitle-adaption ':
                adaption_btn.click()
                print('adapt subtitle')

            time.sleep(600)

        # 暂停演讲
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[1]/div[1]/div/div[1]/div/button[1]/span').click()
        time.sleep(10)
        print("10 click pause")

        # 继续演讲
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[1]/div[1]/div/div[1]/div/button[1]/span').click()
        time.sleep(5)
        print("11 click continue")
