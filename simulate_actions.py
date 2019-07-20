__author__ = "jialin2@iflytek.com"

import threading
import time
import random
# import pysnooper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 循环执行
'''
def actions_loop(driver, count):
    # 定位到最尾的讲话人输入框
    ActionChains(driver).move_to_element(
        driver.find_element_by_xpath('//*[@class="hisee-speaker-list-wrap"]')).perform()
    driver.find_element_by_xpath('//*[@class="hisee-speaker-list"]/div[last()]/span').click()
    # time.sleep(1)

    # 输入讲话人名称
    input = driver.find_element_by_xpath('//*[@class="hisee-speaker-list active"]/div[last()]/input')
    input.send_keys('Speaker' + str(count))
    input.send_keys(Keys.ENTER)
    print("*** " + str(count) + " enter speaker name")

    count += 1

    global timer
    # 等待10s后再次调用执行本方法
    timer = threading.Timer(10, actions_loop, (driver, count,))
    timer.start()

    time.sleep(35)
    timer.cancel()
    print("finish marking speaker")
'''


# 讲话速记模块，模拟用户操作
# @pysnooper.snoop()
def actions4realtime(driver, count):
    # 暂停讲话速记
    driver.find_element_by_xpath('//div[@class="realtime-trans-pause-action"]').click()
    print("pause")
    time.sleep(1)

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
    time.sleep(1)

    # 定位到最尾的讲话人输入框
    ActionChains(driver).move_to_element(
        driver.find_element_by_xpath('//*[@class="hisee-speaker-list-wrap"]')).perform()
    try:
        speaker = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@class="hisee-speaker-list"]/div[last()]/span'))
        )
    except Exception:
        print("speaker span not visible")
    else:
        speaker.click()
        time.sleep(1)

        try:
            # 输入讲话人名称
            input = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@class="hisee-speaker-list active"]/div[last()]/input'))
        )
        except Exception:
            print("speaker input not visible")
        else:
            input.send_keys('Speaker' + str(count))
            input.send_keys(Keys.TAB)
            print("*** " + str(count) + " enter speaker name")
            time.sleep(2)
    finally:
        # 继续讲话速记
        driver.find_element_by_xpath('//div[@class="realtime-trans-continue-action"]').click()
        print("continue")

        driver.execute_script(js)


# 采集卡演讲 & 视频叠加字幕模块，模拟用户操作
def actions4DVRmode(driver):
    print("==========")

    # 在指定范围内生成随机坐标x,y, 预览窗口参数x: 100 y: 120 w: 1086 h: 611
    x = random.randint(100, 1186)
    y = random.randint(120, 731)
    subtitle = driver.find_element_by_class_name('subtitle-preview-container')
    # 拖动预览字幕条到指定位置
    ActionChains(driver).drag_and_drop_by_offset(subtitle, x, y).perform()
    print("drag and drop the subtitle")
    time.sleep(5)

    # 关闭字幕展示，等待5s后再次打开
    switch = driver.find_element_by_xpath('//div[@class="subtitle-switch  "]/i')
    switch.click()
    print("close subtitle")
    time.sleep(5)
    switch.click()
    print("display subtitle")

    # 模拟按下键盘F3，清空字幕
    time.sleep(10)
    driver.find_element_by_xpath('//a[@class="subtitle-edit-action clear-subtitle-action"]').click()
    print("wipe edit content")

    time.sleep(40)
    # 点击一键智能适配，将字幕条位置还原为默认位置
    driver.find_element_by_class_name('subtitle-adaption').click()
    print("restore subtitle position")
    print("action done")
    print("==========")

