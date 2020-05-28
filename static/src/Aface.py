from selenium import webdriver
import time


class Aface():
    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def login_eface(self):
        self.driver.get('https://www.baidu.com')
        self.driver.find_element_by_id('kw').send_keys('鞋子')
        self.driver.find_element_by_id('su').click()
        time.sleep(2)
    
    def login_aface(self, host):
        self.driver.get(host)
        # time.sleep(5)
        # driver.find_elements_by_xpath('//*[@id="user"]').send_keys('001')
        dr = self.driver.find_elements_by_css_selector(
            'html body.bg.row div.col-lg-12.col-xs-12 div.col-lg-3.col-md-4.col-sm-5.col-xs-10.login-boder form#login.login_form.clearfix div.col-lg-9.col-md-9.col-sm-9.user_input input#user.user')
        dr[0].send_keys('001')
        pwd = self.driver.find_elements_by_css_selector('html body.bg.row div.col-lg-12.col-xs-12 div.col-lg-3.col-md-4.col-sm-5.col-xs-10.login-boder form#login.login_form.clearfix div.col-lg-9.col-md-9.col-sm-9 span#pass input#pwd.key')
        pwd[0].send_keys()
        bt = self.driver.find_elements_by_css_selector('html body.bg.row div.col-lg-12.col-xs-12 div.col-lg-3.col-md-4.col-sm-5.col-xs-10.login-boder form#login.login_form.clearfix div.col-lg-9.col-md-9.col-sm-9 input#btnLogin.btn')
        bt[0].click()
        time.sleep(5)
    
    def run(self):
        self.login_eface()
        self.login_aface('http://192.168.11.156:8011')
        self.driver.quit()


if __name__ == '__main__':
    Aface = Aface()
    Aface.run()
