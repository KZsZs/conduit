from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestWebShop(object):
    def setup(self):
        self.driver = webdriver.Chrome("C:\\Windows\\\chromedriver.exe")
        self.driver.get("http://webshop.progmasters.hu")

    def teardown(self):
        self.driver.quit()

    # Test1
    def test__home_page_appearances(self):
        assert self.driver.find_element_by_id("shopName").text == "CsillámPóni Confectionery"

    # Test2
    def test_navigate_to_login(self):
        self.driver.maximize_window()
        self.driver.find_element_by_id("login").click()
        self.driver.find_element_by_id("email").send_keys("admin1@gmail.com")
        self.driver.find_element_by_id("password").send_keys("admin1")
        self.driver.find_element_by_xpath('//button[@class="btn login-btn "]').click()
        element = WebDriverWait(
            self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "category-list-link"))
        )
        assert element.text == "Category List"
