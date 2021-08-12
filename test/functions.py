import csv
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


def xpath(driver, xpath_data):
    return driver.find_element_by_xpath(xpath_data)


def webwait_by_xpath(driver, seconds, xpath_data):
    element = WebDriverWait(driver, seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath_data))
    )
    return element


def webwait_by_id(driver, seconds, id_data):
    element = WebDriverWait(driver, seconds).until(
        EC.presence_of_element_located((By.ID, id_data))
    )
    return element


def accept_cookies(driver):
    time.sleep(3)
    accept_cookie_button = driver.find_element_by_xpath(
        '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    accept_cookie_button.click()
    time.sleep(3)


def logging_in(driver):
    time.sleep(3)
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]'))
    )
    sign_in_button.click()
    login_email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email"]'))
    )
    login_password_field = driver.find_element_by_xpath('//input[@placeholder="Password"]')
    login_email_field.click()
    login_button = driver.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    with open("user_data.csv", "r", encoding='utf-8') as csvfile_read:
        csvreader = csv.reader(csvfile_read.readlines(), delimiter=',')
        next(csvreader)
        for row in csvreader:
            login_email_field.click()
            login_email_field.send_keys(row[1])
            login_password_field.click()
            login_password_field.send_keys(row[2])
            login_button.click()
            break
    time.sleep(5)


def click_new_article(driver):
    article_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="nav-link" and contains(text(),"New Article")]'))
    ).click()
    time.sleep(2)
    article_title = xpath(driver, '//input[@placeholder = "Article Title"]')
    article_about = xpath(driver, "//input[@placeholder = \"What's this article about?\"]")
    article_text = xpath(driver, '//textarea')
    article_tags = xpath(driver, '//input[@placeholder = "Enter tags"]')
    article_publish_button = xpath(driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
    time.sleep(2)


def create_new_article(driver):
    article_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="nav-link" and contains(text(),"New Article")]'))
    ).click()
    time.sleep(2)
    article_title = xpath(driver, '//input[@placeholder = "Article Title"]')
    article_about = xpath(driver, "//input[@placeholder = \"What's this article about?\"]")
    article_text = xpath(driver, '//textarea')
    article_tags = xpath(driver, '//input[@placeholder = "Enter tags"]')
    article_publish_button = xpath(driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
    random_number = random.randint(0, 1000)
    with open("articles.csv", "r", encoding='utf-8') as csvfile_read:
        csvreader = csv.reader(csvfile_read.readlines(), delimiter=',')
        next(csvreader)
        for row in csvreader:
            article_title.click()
            article_title.send_keys(row[0] + str(random_number))
            article_about.click()
            article_about.send_keys(row[1])
            article_text.click()
            article_text.send_keys(row[2])
            article_tags.click()
            article_tags.send_keys(row[3])
            break

    xpath(driver, "//html").click()
    time.sleep(2)
    article_publish_button.click()
    time.sleep(2)
