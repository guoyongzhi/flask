from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get('https://www.baidu.com')
driver.find_element_by_id('kw').send_keys('鞋子')
driver.find_element_by_id('su').click()
time.sleep(5)
driver.quit()

driver = webdriver.Ie()
driver.get('https://www.baidu.com')
driver.maximize_window()
time.sleep(5)
driver.quit()


