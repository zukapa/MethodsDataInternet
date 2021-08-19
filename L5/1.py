from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs


client = MongoClient('127.0.0.1', 27017)
db = client['emails']
mail_db = db.mail
driver = webdriver.Chrome()
driver.get("https://mail.ru/")
login = driver.find_element_by_class_name('email-input')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.ENTER)
pass_wait = WebDriverWait(driver, 15)
pass_click = pass_wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
pass_click.send_keys('NextPassword172!?')
pass_click.send_keys(Keys.ENTER)
emails_all = []
emails_all_db = []
while True:
    emails_wait = WebDriverWait(driver, 15)
    emails_wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'js-letter-list-item')))
    emails = driver.find_elements_by_class_name('js-letter-list-item')
    if len(emails) < 30:
        actions = ActionChains(driver)
        actions.move_to_element(emails[-1])
        actions.perform()
        emails = driver.find_elements_by_class_name('js-letter-list-item')
        if len(emails_all) != 0:
            for em in emails:
                href = em.get_attribute('href')
                if emails_all.count(href) == 1:
                    continue
                if emails_all.count(href) == 0:
                    emails_all.append(href)
            break
    if len(emails) == 30:
        emails = emails[-7:]
    for email in emails:
        emails_all.append(email.get_attribute('href'))
    actions = ActionChains(driver)
    actions.move_to_element(emails[-1])
    actions.perform()
for email in emails_all:
    mail = {}
    driver.get(email)
    email_wait = WebDriverWait(driver, 30)
    from_letter_wait = email_wait.until(ec.presence_of_element_located((
        By.XPATH, "//div[@class='letter__author']/span")))
    from_letter = driver.find_element_by_xpath("//div[@class='letter__author']/span").get_attribute('title')
    date_letter_wait = email_wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='letter__date']")))
    date_letter = driver.find_element_by_xpath("//div[@class='letter__date']").text
    subject_letter_wait = email_wait.until(ec.presence_of_element_located((By.XPATH, "//h2[@class='thread__subject']")))
    subject_letter = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
    text_letter_wait = email_wait.until(ec.presence_of_element_located((
        By.XPATH, "//div[@class='js-helper js-readmsg-msg']")))
    soup = bs(driver.page_source, 'html.parser')
    text_letter = soup.find('div', attrs={'class': 'js-helper js-readmsg-msg'}).encode('utf-8')
    mail['from'] = from_letter
    mail['date'] = date_letter
    mail['subject'] = subject_letter
    mail['text'] = text_letter.decode('utf-8')
    emails_all_db.append(mail)
mail_db.insert_many(emails_all_db)
