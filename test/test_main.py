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


def find_xpath(driver, xpath_data):
    return driver.find_element_by_xpath(xpath_data)


def find_id(driver, id_data):
    return driver.find_elements_by_id(id_data)


def webwait_by_xpath(driver, seconds, xpath_data):
    element =  WebDriverWait(driver, seconds).until(
        EC.presence_of_element_located((By.XPATH, xpath_data))
    )
    return element


def webwait_by_id(driver, seconds, id_data):
    WebDriverWait(driver, seconds).until(
        EC.presence_of_element_located((By.ID, id_data))
    )


def accept_cookies(driver):
    time.sleep(3)
    accept_cookie_button = driver.find_element_by_xpath(
        '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    accept_cookie_button.click()
    time.sleep(3)


def logging_out(driver):
    driver.find_element_by_xpath('//*[@class="nav-link" and contains(text(),"Log out")]').click()
    time.sleep(2)


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
    article_title = find_xpath(driver, '//input[@placeholder = "Article Title"]')
    article_about = find_xpath(driver, "//input[@placeholder = \"What's this article about?\"]")
    article_text = find_xpath(driver, '//textarea')
    article_tags = find_xpath(driver, '//input[@placeholder = "Enter tags"]')
    article_publish_button = find_xpath(driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
    time.sleep(2)


def create_new_article(driver):
    article_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="nav-link" and contains(text(),"New Article")]'))
    ).click()
    time.sleep(2)
    article_title = find_xpath(driver, '//input[@placeholder = "Article Title"]')
    article_about = find_xpath(driver, "//input[@placeholder = \"What's this article about?\"]")
    article_text = find_xpath(driver, '//textarea')
    article_tags = find_xpath(driver, '//input[@placeholder = "Enter tags"]')
    article_publish_button = find_xpath(driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
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

    find_xpath(driver, "//html").click()
    time.sleep(2)
    article_publish_button.click()
    time.sleep(2)


############################# Conduit Pytest Setup #############################
class TestConduit(object):
    def setup(self):
        driver_options = Options()
        driver_options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
        self.driver.get("http://localhost:1667/#/")
        time.sleep(1)

    def teardown(self):
        self.driver.quit()

    ############################# Test 1 - Page Load successful #############################
    # def test__page_load(self):
    #     r = requests.get("http://localhost:1667/#/")
    #     assert int(r.status_code) == 200
    #     page_title = find_xpath(self.driver, '//title')
    #     assert page_title.get_attribute("text") == "Conduit"
    #     print("Test 1 - Page load successful")

    # ############################# Test 2 - Accepting Cookies #############################

    # def test__accepting_cookies(self):
    #     cookie_panel = webwait_by_id(self.driver, 10, 'cookie-policy-panel')
    #     accept_cookie_button = self.driver.find_element_by_xpath(
    #         '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    #     accept_cookie_button.click()
    #     time.sleep(2)
    #     assert self.driver.find_elements_by_id('cookie-policy-panel') == []
    #
    #     print("Test 2 - Cookies accepted!")

    ############################# Test 3 - Registration #############################
    def test__registration(self):
        accept_cookies(self.driver)
        signup_field = find_xpath(self.driver, '//a[@href="#/register"]')
        signup_field.click()
        username_field = find_xpath(self.driver, '//input[@placeholder="Username"]')
        email_field = find_xpath(self.driver, '//input[@placeholder="Email"]')
        password_field = find_xpath(self.driver, '//input[@placeholder="Password"]')
        register_button = find_xpath(self.driver, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        with open("user_data.csv", "r", encoding='utf-8') as csvfile_read:
            csvreader = csv.reader(csvfile_read.readlines(), delimiter=',')
            next(csvreader)
            for row in csvreader:
                username_field.click()
                username_field.send_keys(row[0])
                email_field.click()
                email_field.send_keys(row[1])
                password_field.click()
                password_field.send_keys(row[2])
                register_button.click()
                break

        webwait_by_xpath(self.driver, 10, '//div[text()="Your registration was successful!"]')
        registration_text = find_xpath(self.driver, '//div[text()="Your registration was successful!"]')
        assert registration_text.text == "Your registration was successful!"

        time.sleep(2)
        ok_button = self.driver.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        ok_button.click()
        print("Test 3 - Registration succesful")

    ############################# Test 4 - Logging in #############################
    # def test__login(self):
    #     accept_cookies(self.driver)
    #     sign_in_button = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]'))
    #     )
    #     sign_in_button.click()
    #     login_email_field = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email"]'))
    #     )
    #     login_password_field = self.driver.find_element_by_xpath('//input[@placeholder="Password"]')
    #     login_email_field.click()
    #     login_button = self.driver.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    #     with open("user_data.csv", "r", encoding='utf-8') as csvfile_read:
    #         csvreader = csv.reader(csvfile_read.readlines(), delimiter=',')
    #         next(csvreader)
    #         for row in csvreader:
    #             login_email_field.click()
    #             login_email_field.send_keys(row[1])
    #             login_password_field.click()
    #             login_password_field.send_keys(row[2])
    #             login_button.click()
    #             break
    #     time.sleep(5)
    #     log_out_button = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@class="nav-link" and contains(text(),"Log out")]'))
    #     )
    #     assert log_out_button.text == " Log out"
    #
    #     print("Test 4 - Logging in successful")

    ############################# Test 5 - Create Article #############################
    # def test__create_article(self):
    #     accept_cookies(self.driver)
    #     logging_in(self.driver)
    #     new_article_button = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@class="nav-link" and contains(text(),"New Article")]'))
    #     ).click()
    #     time.sleep(2)
    #     assert self.driver.current_url == "http://localhost:1667/#/editor"
    #     article_title = find_xpath(self.driver, '//input[@placeholder = "Article Title"]')
    #     article_about = find_xpath(self.driver, "//input[@placeholder = \"What's this article about?\"]")
    #     article_text = find_xpath(self.driver, '//textarea')
    #     article_tags = find_xpath(self.driver, '//input[@placeholder = "Enter tags"]')
    #     article_publish_button = find_xpath(self.driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
    #
    #     with open("articles.csv", "r", encoding='utf-8') as csvfile_read:
    #         csvreader = csv.reader(csvfile_read.readlines(), delimiter=',')
    #         next(csvreader)
    #         for row in csvreader:
    #             title = row[0]
    #             article_title.click()
    #             article_title.send_keys(row[0])
    #             article_about.click()
    #             article_about.send_keys(row[1])
    #             article_text.click()
    #             article_text.send_keys(row[2])
    #             article_tags.click()
    #             article_tags.send_keys(row[3])
    #             break
    #
    #     find_xpath(self.driver, "//html").click()
    #     time.sleep(2)
    #     article_publish_button.click()
    #     article_url = "http://localhost:1667/#/articles/" + title.lower()
    #     time.sleep(2)
    #     assert self.driver.current_url == article_url
    #
    #     print("Test 5 - Creating an article successful")

    # ############################# Test 6 - Repeated article creation #############################

    # def test__repeated_article_creation(self):
    #     accept_cookies(self.driver)
    #     logging_in(self.driver)
    #     with open("articles.csv", "r", encoding='utf-8') as csvfile_read:
    #         csvreader = csv.reader(csvfile_read.readlines(), delimiter=',')
    #         next(csvreader)
    #         for i in range(5):
    #             click_new_article(self.driver)
    #             article_title = find_xpath(self.driver, '//input[@placeholder = "Article Title"]')
    #             article_about = find_xpath(self.driver, "//input[@placeholder = \"What's this article about?\"]")
    #             article_text = find_xpath(self.driver, '//textarea')
    #             article_tags = find_xpath(self.driver, '//input[@placeholder = "Enter tags"]')
    #             article_publish_button = find_xpath(self.driver,
    #                                                 "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
    #             for row in csvreader:
    #                 title = row[0]
    #                 article_title.click()
    #                 article_title.send_keys(row[0])
    #                 article_about.click()
    #                 article_about.send_keys(row[1])
    #                 article_text.click()
    #                 article_text.send_keys(row[2])
    #                 article_tags.click()
    #                 article_tags.send_keys(row[3])
    #                 last_title = row[0]
    #                 break
    #             find_xpath(self.driver, "//html").click()
    #             time.sleep(2)
    #             article_publish_button.click()
    #     time.sleep(2)
    #     last_article_url = "http://localhost:1667/#/articles/" + last_title.lower()
    #     print(last_article_url)
    #     time.sleep(2)
    #     assert self.driver.current_url == last_article_url
    #
    #     print("Test 6 - Creating articles from file successful")

    # ############################# Test 7 - Editing Article #############################
    #
    # def test__editing_article(self):
    #     accept_cookies(self.driver)
    #     logging_in(self.driver)
    #     create_new_article(self.driver)
    #     edit_article_button = find_xpath(self.driver, '//a[@class = "btn btn-sm btn-outline-secondary"]')
    #     edit_article_button.click()
    #     time.sleep(3)
    #     # title_field = webwait_by_xpath(self.driver, 10, '//input[@placeholder = "Article Title"]')
    #     text_field_to_edit = find_xpath(self.driver, '//textarea')
    #     article_publish_button = find_xpath(self.driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
    #     text_field_to_edit.clear()
    #     text_field_to_edit.click()
    #     text_field_to_edit.send_keys("Edited test content")
    #     text_field_to_edit.send_keys(Keys.ENTER)
    #     article_publish_button.click()
    #     time.sleep(2)
    #     edited_content = find_xpath(self.driver, "//div[@class = 'row article-content']/div/div/p")
    #     assert edited_content.text == "Edited test content"
    #
    #     print("Test 7 - Editing article successful")
    #
    # ############################# Test 8 - Delete Article #############################
    #
    # def test__delete_article(self):
    #     accept_cookies(self.driver)
    #     logging_in(self.driver)
    #     article_button = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@class="nav-link" and contains(text(),"New Article")]'))
    #     ).click()
    #     time.sleep(2)
    #     article_title = find_xpath(self.driver, '//input[@placeholder = "Article Title"]')
    #     article_about = find_xpath(self.driver, "//input[@placeholder = \"What's this article about?\"]")
    #     article_text = find_xpath(self.driver, '//textarea')
    #     article_tags = find_xpath(self.driver, '//input[@placeholder = "Enter tags"]')
    #     article_publish_button = find_xpath(self.driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
    #     article_title.click()
    #     article_title.send_keys("NewArticleToDelete")
    #     article_about.click()
    #     article_about.send_keys("About to delete")
    #     article_text.click()
    #     article_text.send_keys("Text to delete")
    #     article_tags.click()
    #     article_tags.send_keys("Tag to delete")
    #     find_xpath(self.driver, "//html").click()
    #     time.sleep(2)
    #     article_publish_button.click()
    #     time.sleep(2)
    #     title_of_article_to_delete = find_xpath(self.driver, '//h1')
    #     print(title_of_article_to_delete.text)
    #     main_window = self.driver.window_handles[0]
    #     delete_article_button = find_xpath(self.driver, '//button[@class = "btn btn-outline-danger btn-sm"]')
    #     delete_article_button.click()
    #     time.sleep(2)
    #     self.driver.execute_script("window.open('http://localhost:1667/#/articles/newarticletodelete')")
    #     deleted_article_window = self.driver.window_handles[1]
    #     self.driver.switch_to.window(deleted_article_window)
    #     time.sleep(2)
    #     deleted_article_title = find_xpath(self.driver, '//h1')
    #     assert deleted_article_title.text == ''
    #     self.driver.close()
    #     self.driver.switch_to.window(main_window)
    #
    #     print("Test 8 - Deleting Article successful")
    #
    # ############################# Test 9 - Save article to document #############################
    #
    # def test__save_to_file(self):
    #     accept_cookies(self.driver)
    #     logging_in(self.driver)
    #     create_new_article(self.driver)
    #     article_title = find_xpath(self.driver, '//*[@id="app"]/div/div[1]/div/h1')
    #     article_author = find_xpath(self.driver, '//a[@class="author"]')
    #     article_text = find_xpath(self.driver, '//*[@id="app"]/div/div[2]/div[1]/div/div[1]/p')
    #     article_tag = find_xpath(self.driver, '//a[@class="tag-pill tag-default"]')
    #     article_data = [article_title, article_author, article_text, article_tag]
    #     with open("article_data.txt", 'w') as file_write:
    #         for i in range(4):
    #             file_write.write(article_data[i].text + '\n')
    #     with open("article_data.txt", 'r') as file_read:
    #         for i in range(4):
    #             read_lines = file_read.readline()
    #             assert read_lines == (article_data[i].text + '\n')
    #     print("Test 9 - Save article to document successful")
    #
    # ############################# Test 10 - List Articles #############################
    #
    def test__list_articles(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        user_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/nav/div/ul/li[4]/a'))
        )
        user_button.click()
        preview_list = self.driver.find_elements_by_xpath('//a[@class="preview-link"]')
        number_of_article_previews = len(preview_list)
        number_of_articles = 0
        for article in preview_list:
            number_of_articles += 1
        assert number_of_articles == number_of_article_previews
        print("Test 10 - Listing Content successful")
    #
    # ############################# Test 11 - Pagination #############################
    #
    # def test__pagination(self):
    #     accept_cookies(self.driver)
    #     logging_in(self.driver)
    #     user_button = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/nav/div/ul/li[4]/a'))
    #     )
    #     user_button.click()
    #     time.sleep(2)
    #     article_page_list = self.driver.find_elements_by_class_name("page-link")
    #     last_page_number = 0
    #     for page in article_page_list:
    #         page.click()
    #         last_page_number = int(page.text)
    #     assert last_page_number == len(article_page_list)
    #
    #     print("Test 11 - Pagination successful!")
    #
    # ############################# Test 12 - Log out #############################
    #
    # def test__logout(self):
    #     accept_cookies(self.driver)
    #     logging_in(self.driver)
    #     log_out_button = webwait_by_xpath(self.driver, 5, '//*[@class="nav-link" and contains(text(),"Log out")]')
    #     # log_out_button = WebDriverWait(self.driver, 10).until(
    #     #     EC.presence_of_element_located((By.XPATH, '//*[@class="nav-link" and contains(text(),"Log out")]'))
    #     # )
    #
    #     assert log_out_button.text == " Log out"
    #     log_out_button.click()
    #     sign_up_field = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]'))
    #     )
    #     assert sign_up_field.text == "Sign up"
    #     print("Test 12 - Logging out successful")
