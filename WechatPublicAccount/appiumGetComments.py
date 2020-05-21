# coding=utf-8
import json
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def appiumServer():
    # appium服务监听地址
    server = 'http://localhost:4723/wd/hub'  # localhost为本机；4723为端口；/wd/hub可以看成是规定的默认地址
    # app启动参数
    desired_caps = {
        "platformName": "Android",  # platformName：使用哪个移动操作系统平台；iOS，Android或FirefoxOS
        "deviceName": "127.0.0.1:7555",  # deviceName：使用的移动设备或模拟器的种类
        "appPackage": "com.tencent.mm",  # appPackage：你想运行的Android应用程序的Java包（仅限Android使用）
        "appActivity": "com.tencent.mm.ui.LauncherUI",  # 要从包中启动的Android活动的活动名称。（仅限Android使用）
        'noReset': "True"
    }
    # 驱动
    driver = webdriver.Remote(server, desired_caps)
    wait = WebDriverWait(driver, 1)
    # 获取聊天记录 layout
    while True:
        try:
            time.sleep(2)
            # 找到微信聊天中聊天记录的第一个对象
            messageLayout = wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/b4r")))
            # 如果存在聊天对象
            # 是否有红色的小标记（记录未读消息数）
            try:
                newMessageIcon = messageLayout.find_element_by_xpath('//*[@class="android.widget.LinearLayout"]//android.widget.TextView')
                # 从聊天列表页（聊天详情页外）看到的消息简介
                shortMessage = messageLayout.find_elements_by_xpath('//*[@class="android.widget.LinearLayout"]//android.view.View')[-1].text
                rticleID = shortMessage.split('/')[-1][:10]

                # 如果存在未读消息，且 消息简介中包含了 'https://mp.weixin.qq.com/s/'(微信公众号文章链接前缀)
                # 则点击链接，打开文章，mitmproxy捕获到评论，关机文章、关闭聊天、回到聊天聊表页待命。
                if newMessageIcon and 'https://mp.weixin.qq.com/s/' in shortMessage:
                    # 点击聊天、进入聊天详情页
                    messageLayout.click()
                    # 点击聊天记录 进入文章详情页。
                    wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/ala")))
                    # print('messageView', messageView)
                    # messageView.click()
                    TouchAction(driver).press(x=380, y=278).release().perform()
                    # TouchAction(driver).tap(x=190, y=274).perform()
                    # wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/ala"))).click()
                    time.sleep(7)
                    getComments(rticleID)
                    # 关闭文章，回到聊天详情页
                    # wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/dn"))).click()
                    driver.back()
                    # 关闭聊天详情页，回到聊天列表页
                    driver.back()
                    # wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/rs"))).click()
            except:
                messageLayout = wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/b4r")))
                TouchAction(driver).long_press(messageLayout).perform()
                driver.find_element_by_xpath("//*[@text='删除该聊天']").click()
                driver.find_element_by_xpath("//*[@text='删除']").click()
        except:
            time.sleep(2)
        finally:
            time.sleep(2)


def getComments(rticleID):
    print('http://127.0.0.1:5000/?id=' + rticleID)
    with open('comments.json', 'r', encoding='utf-8') as R:
        commentsJson = str(R.read())
    with open(rticleID + '-comments.json', 'w', encoding='utf-8') as W:
        W.write(commentsJson)


if __name__ == '__main__':
    appiumServer()
