from selenium.webdriver.chrome.webdriver import WebDriver

__author__ = "jialin2@iflytek.com"

import time
import xlsxwriter
import socket

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# 输入单条稳定性测试记录的grafana面板链接
# 示例：http://172.31.205.34:3000/d/gCmdndkZz/telegraf-and-influx-windows-host-overview?orgId=1&var-hostname=DESKTOP-LCH09QG&var-disk=All&var-process=All&var-network=All&from=1562068320000&to=1562115780000
url = input('Enter the Grafana link of record: ')

# "D:\Python37-32\chromedriver.exe"
driver = webdriver.Chrome()
driver.maximize_window()

# 访问grafana平台
driver.get(url)

# 输入账密后登陆
username = driver.find_element_by_xpath('//input[@name="username"]')
username.send_keys('admin')
password = driver.find_element_by_xpath('//input[@name="password"]')
password.send_keys('admin123')
driver.find_element_by_xpath('//div[@class="login-button-group"]/button').click()
time.sleep(5)

'''
# 等待页面加载完毕，导航条"Home"按钮可见
navbar = WebDriverWait(driver, 30, 2).until(
        EC.visibility_of_element_located((By.XPATH, '//a[@class="navbar-page-btn"]'))
)
# 点击Home按钮，打开搜索栏
navbar.click()

# 搜索并打开dashboard "Telegraf & Influx Windows Host Overview"
search = driver.find_element_by_xpath('//div[@class="search-field-wrapper"]/input')
search.send_keys('telegraf')
search.send_keys(Keys.ENTER)
time.sleep(10)

# 获取主机名
# hostname = socket.gethostname()
hostname = 'DESKTOP-5I3Q2AQ'

# 点击Hostname下拉菜单并输入主机名，选中筛选出的选项
driver.find_element_by_xpath('//a[@class="variable-value-link"]').click()
driver.find_element_by_xpath('//div[@class="variable-value-link"]/input').send_keys(hostname)
time.sleep(1)
driver.find_element_by_xpath('//a[@class="variable-option pointer selected"]').click()
time.sleep(3)
'''

driver.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);

            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }

            setTimeout(f, 1000);
        })();
    """)

for i in xrange(30):
    if "scroll-done" in driver.title:
        break
    time.sleep(10)

driver.save_screenshot('screenshot.png')
print('take screenshot')
