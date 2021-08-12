import time
import schedule
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 加启动配置 禁用日志log
chrome_opt = Options()
# –no - sandbox 参数是让root权限下跑
chrome_opt.add_argument('–no-sandbox')
chrome_opt.add_argument('--start-maximized')  # 最大化
chrome_opt.add_argument('--incognito')  # 无痕隐身模式
chrome_opt.add_argument("disable-cache")  # 禁用缓存
chrome_opt.add_argument('log-level=3')
chrome_opt.add_argument('disable-infobars')
chrome_opt.add_argument('--headless')


class SeuDaKa(object):
    def __init__(self):
        # 打卡网址
        self.login_url = "https://newids.seu.edu.cn/authserver/login?service=http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/*default/index.do"
        # 登出网址
        self.logout_url = "https://newids.seu.edu.cn/authserver/index.do"
        self.browser = webdriver.Chrome(options=chrome_opt)

    def login(self, username, password):
        self.browser.get(self.login_url)
        # 等待用户名和密码框加载完成
        username_field = WebDriverWait(self.browser, 15, 0.5).until(
            EC.presence_of_element_located((By.ID, 'username')))
        password_field = WebDriverWait(self.browser, 15, 0.5).until(
            EC.presence_of_element_located((By.ID, 'password')))
        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button = self.browser.find_element_by_class_name('auth_login_btn')
        login_button.submit()
        # 等待打卡页面加载完成（这里是看"基本信息上报"是否加载完成）
        self.wait_by_xpath('//*[@id="app"]/div/div[1]/button')

    def wait_by_xpath(self, loc, timeout=15):
        return WebDriverWait(self.browser, timeout, 0.5).until(EC.presence_of_element_located((By.XPATH, loc)))

    def logout(self):
        # 坑人的 SEU 会记录登录的ip和浏览器导致即使关闭标签页也无法退出登录，为下一位同学的登录带来问题
        self.browser.get(self.logout_url)  # 这是登录认证界面
        logout_button = WebDriverWait(self.browser, 15, 0.5).until(
            EC.presence_of_element_located((By.ID, 'logout')))
        if logout_button:
            logout_button.click()
        return self.browser

    def report(self):
        # 检查是否存在新增按钮
        time.sleep(1)
        buttons = self.browser.find_elements_by_tag_name('button')
        daily_done = True
        for button in buttons:
            if button.get_attribute("textContent").find("新增") >= 0:
                new_button = button
                daily_done = False
                break

        # 检查是否存在退出按钮
        exit_button = self.browser.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/button')

        if daily_done is True and exit_button:  # 今日已完成打卡
            print("今日已完成打卡任务")

        elif daily_done is False and exit_button:  # 今日未完成打卡
            # 点击报平安
            new_button.click()
            time.sleep(2)
            # 输入当天晨检体温, 36.5-37之间的随机值
            input_filed = self.wait_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div/div[4]/div/div[2]/div[1]/div/a/div[2]/div[2]/input')
            input_filed.click()
            input_filed.send_keys(str(random.randint(365, 370) / 10.0))
            submit_button = self.browser.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[3]/button')
            submit_button.click()
            time.sleep(1)
            # 提交
            confirm_buttons = (self.browser.find_elements_by_tag_name('button'))[-1]
            if confirm_buttons.get_attribute("textContent").find("确定") >= 0:
                confirm_buttons.click()
                # 确认"基本信息上报"加载完成
                if self.wait_by_xpath('//*[@id="app"]/div/div[2]/a[2]/div[2]'):
                    daily_done = True  # 标记已完成打卡
                    print("打卡成功")
                else:
                    print("网站出现故障")
            else:
                print("本次打卡失败,无法点击提交按钮")
        return daily_done

    def daily_report(self):
        # username and password
        print("Start Report")
        # read user.txt as username and password
        # filename = 'DailyReport/user.txt'
        filename = 'user.txt'
        file = open(filename)
        user = file.readlines()
        file.close()
        for i in user:
            person = i.split(',')
            self.login(person[0], person[1].split('\n')[0])
            self.report()
            self.logout()
        print("End Report")


def main():
    test = SeuDaKa()
    schedule.every().day.at("06:00").do(test.daily_report)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
