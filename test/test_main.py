from functions import *

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
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_01 pontja alatt.
    # ATC_01 Step 01: Oldal megnyitasa.
    def test__page_load(self):
        # ATC_01 Step 02: Ellenorizzuk a betoltott oldal Response kodjat.
        r = requests.get("http://localhost:1667/#/")
        assert int(r.status_code) == 200
        # ATC_01 Step 03: Ellenorizzuk, hogy a Conduit oldal toltott be a html title tag-jenek vizsgalataval.
        page_title = xpath(self.driver, '//title')
        assert page_title.get_attribute("text") == "Conduit"
        print("Test 1 - Page load successful")

    ############################# Test 2 - Accepting Cookies #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_02 szam alatt.
    # ATC_02 Step 01: Oldal megnyitasa.
    def test__accepting_cookies(self):
        # ATC_02 STEP 02: Az oldal betoltesevel megjelenik a sutik elfogadasat lehetove tevo felulet.
        cookie_panel = webwait_by_id(self.driver, 10, 'cookie-policy-panel')
        # ATC_02 STEP 03+04: Megjelenik az ’I accept!’ sutik elfogadasat lehetove tevo gomb, kattintsunk ra.
        accept_cookie_button = self.driver.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        accept_cookie_button.click()
        time.sleep(2)
        # ATC_02 STEP 05: Ellenorizzuk, hogy a sutik elfogadasat lehetove tevo felulet mar nem jelenik meg.
        assert self.driver.find_elements_by_id('cookie-policy-panel') == []

        print("Test 2 - Cookies accepted!")

    ############################# Test 3 - Registration #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_03 szam alatt.
    # ATC_03 Step 01: Oldal megnyitasa + Sutik elfogadasa.
    def test__registration(self):
        accept_cookies(self.driver)
        # ATC_03 Step 02+03: A regisztraciot lehetove tevo ’Sign up’ gomb megjelenik, majd kattintsunk ra.
        signup_field = xpath(self.driver, '//a[@href="#/register"]')
        signup_field.click()
        # ATC_03 Step 04: Ellenorizzük, hogy a regisztracios feluleten megtalalhatoak a kovetkezo elemek:
        # •	’Username’ beviteli mezo
        # •	’Email’ beviteli mezo
        # •	’Password’ beviteli mezo
        # •	’Sign up’ gomb
        username_field = xpath(self.driver, '//input[@placeholder="Username"]')
        email_field = xpath(self.driver, '//input[@placeholder="Email"]')
        password_field = xpath(self.driver, '//input[@placeholder="Password"]')
        register_button = xpath(self.driver, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        # ATC_03 Step 05: Regisztraljunk file-ból kiolvasott, helyes adatokkal:
        # o	Felhasználónév: LezerGeza
        # o	E-mail cím: lezergeza@gmail.com
        # o	Jelszó: ABCdefg123
        # •	Indítsuk el a regisztrációt a Sign Up gombra kattintva
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

        time.sleep(5)
        # ATC_03 Step 06: Ellenorizzuk, a sikeres regisztraciot a regisztracios felugro ablak szovegeben.
        registration_text = xpath(self.driver, '//div[text()="Your registration was successful!"]')
        assert registration_text.text == "Your registration was successful!"

        time.sleep(2)
        ok_button = self.driver.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        ok_button.click()
        print("Test 3 - Registration succesful")

    ############################# Test 4 - Logging in #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_04 szam alatt.
    # ATC_04 Step 01: Oldal megnyitasa + Sutik elfogadasa.
    def test__login(self):
        accept_cookies(self.driver)
        #ATC_04 Step 02-03: A bejelentkezeshez szükseges ’Sign in’ gomb megjelenik, majd kattintsunk ra.
        sign_in_button = webwait_by_xpath(self.driver, 10, '//a[@href="#/login"]')
        sign_in_button.click()
        #ATC_05 Step 04: Jelentkezzunk be korabban regisztralt, dokumentumbol kiolvasott felhasznaloi adatokkal:
        # Email cim: lezergeza@gmail.com
        # Jelszo: ABCdefg123
        # Inditsuk el a bejelentkezest a ’Sign in’ gombra kattintva
        login_email_field = webwait_by_xpath(self.driver, 10, '//input[@placeholder="Email"]')
        login_password_field = xpath(self.driver, '//input[@placeholder="Password"]')
        login_email_field.click()
        login_button = xpath(self.driver, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
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
        # ATC_04 Step 05: Ellenorizzuk, hogy valoban sikeres volt a bejelentkezes a "Log out" gomb megjelenésével.
        log_out_button = webwait_by_xpath(self.driver, 10, '//*[@class="nav-link" and contains(text(),"Log out")]')
        assert log_out_button.text == " Log out"

        print("Test 4 - Logging in successful")

    ############################# Test 5 - Create Article #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_05 szam alatt.
    # ATC_05 Step 01: Oldal megnyitasa + Sutik elfogadasa + Bejelentkezes.
    def test__create_article(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        # ATC_05 Step 02-03: Ellenorizzuk a ’New Article’ gomb megjeleneset, majd kattintsunk ra.
        new_article_button = webwait_by_xpath(self.driver, 10,
                                              '//*[@class="nav-link" and contains(text(),"New Article")]')
        new_article_button.click()
        time.sleep(2)
        assert self.driver.current_url == "http://localhost:1667/#/editor"
        # ATC_05 Step 04: Ellenorizzuk, hogy a cikk letrehozasat lehetove tevo oldalon megjelennek a kovetkezo elemek:
        # Cikk cím beviteli mező
        # Témamegjelölés beviteli mező
        # Cikk szövege beviteli mező
        # Tag-ek megadására szolgáló beviteli mező
        # Cikk publikálását lehetővé tevő gomb
        article_title = xpath(self.driver, '//input[@placeholder = "Article Title"]')
        article_about = xpath(self.driver, "//input[@placeholder = \"What's this article about?\"]")
        article_text = xpath(self.driver, '//textarea')
        article_tags = xpath(self.driver, '//input[@placeholder = "Enter tags"]')
        article_publish_button = xpath(self.driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
        # ATC_05 Step 05: Hozzunk letre uj cikket minden mezo kitoltesesvel. Az adatokat dokumentumbol olvassuk be:
        # Article title: „TestTitle”
        # About: „TestAbout”
        # Article content: „TestText”
        # Tag: „TestTag”
        # Kattintsunk a ’Publish Article’ gombra
        with open("articles.csv", "r", encoding='utf-8') as csvfile_read:
            csvreader = csv.reader(csvfile_read.readlines(), delimiter=',')
            next(csvreader)
            for row in csvreader:
                title = row[0]
                article_title.click()
                article_title.send_keys(row[0])
                article_about.click()
                article_about.send_keys(row[1])
                article_text.click()
                article_text.send_keys(row[2])
                article_tags.click()
                article_tags.send_keys(row[3])
                break

        xpath(self.driver, "//html").click()
        time.sleep(2)
        article_publish_button.click()
        #ATC_05 Step 06: Ellenorizzuk, hogy a cikk cimeben megadott szoveg megegyezik az URL utolso elemevel.
        article_url = "http://localhost:1667/#/articles/" + title.lower()
        time.sleep(2)
        assert self.driver.current_url == article_url

        print("Test 5 - Creating an article successful")

    ############################# Test 6 - Repeated article creation #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_06 szam alatt.
    # ATC_06 Step 01: Oldal megnyitasa + Sutik elfogadasa + Bejelentkezes.
    def test__repeated_article_creation(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        # ATC_06 Step 02-03: Egy csv dokumentumbol olvassuk ki es illeszünk be az adatokat.
        # Minden iteracio a 'New Article' gomb megnyomasaval kezdodik es a ’Publish Article’ gomb megnyomasaval zarul.
        with open("articles.csv", "r", encoding='utf-8') as csvfile_read:
            csvreader = csv.reader(csvfile_read.readlines(), delimiter=',')
            next(csvreader)
            for i in range(5):
                click_new_article(self.driver)
                article_title = xpath(self.driver, '//input[@placeholder = "Article Title"]')
                article_about = xpath(self.driver, "//input[@placeholder = \"What's this article about?\"]")
                article_text = xpath(self.driver, '//textarea')
                article_tags = xpath(self.driver, '//input[@placeholder = "Enter tags"]')
                article_publish_button = xpath(self.driver,
                                               "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
                for row in csvreader:
                    title = row[0]
                    article_title.click()
                    article_title.send_keys(row[0])
                    article_about.click()
                    article_about.send_keys(row[1])
                    article_text.click()
                    article_text.send_keys(row[2])
                    article_tags.click()
                    article_tags.send_keys(row[3])
                    last_title = row[0]
                    break
                xpath(self.driver, "//html").click()
                time.sleep(2)
                article_publish_button.click()
        time.sleep(2)
        # ATC_06 Step 04: Az adatbevitel sikeresseget ellenorizzuk az utolso cikk url-jenek es a dokumentum utolsó
        # soraban talalhato cim adat osszevetesevel.
        last_article_url = "http://localhost:1667/#/articles/" + last_title.lower()
        print(last_article_url)
        time.sleep(2)
        assert self.driver.current_url == last_article_url

        print("Test 6 - Creating articles from file successful")

    ############################# Test 7 - Editing Article #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_07 szam alatt.
    # ATC_07 Step 01: Oldal megnyitasa + Sutik elfogadasa + Bejelentkezes + uj cikk letrehozasa.

    def test__editing_article(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        create_new_article(self.driver)
        # ATC_07 Step 02-03: Ellenorizzuk az ’Edit article’ gomb megjeleneset, majd kattintsunk ra.
        edit_article_button = xpath(self.driver, '//a[@class = "btn btn-sm btn-outline-secondary"]')
        edit_article_button.click()
        time.sleep(3)
        # ATC_07 Step 04: Modositsuk a cikk egyik adatat: Article content = „Edited test content”.
        text_field_to_edit = xpath(self.driver, '//textarea')
        article_publish_button = xpath(self.driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
        text_field_to_edit.clear()
        text_field_to_edit.click()
        text_field_to_edit.send_keys("Edited test content")
        text_field_to_edit.send_keys(Keys.ENTER)
        article_publish_button.click()
        time.sleep(2)
        # ATC_07 Step 05: Vessuk ossze az 'Article content' elem tartalmat a szerkesztesekor bevitt adattal.
        edited_content = xpath(self.driver, "//div[@class = 'row article-content']/div/div/p")
        assert edited_content.text == "Edited test content"

        print("Test 7 - Editing article successful")

    ############################# Test 8 - Delete Article #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_08 szam alatt.
    # ATC_08 Step 01: Oldal megnyitasa + Sutik elfogadasa + Bejelentkezes + uj cikk letrehozasa.
    def test__delete_article(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        article_button = webwait_by_xpath(self.driver, 10,
                                          '//*[@class="nav-link" and contains(text(),"New Article")]').click()
        time.sleep(2)
        article_title = xpath(self.driver, '//input[@placeholder = "Article Title"]')
        article_about = xpath(self.driver, "//input[@placeholder = \"What's this article about?\"]")
        article_text = xpath(self.driver, '//textarea')
        article_tags = xpath(self.driver, '//input[@placeholder = "Enter tags"]')
        article_publish_button = xpath(self.driver, "//button[@class= 'btn btn-lg pull-xs-right btn-primary']")
        article_title.click()
        article_title.send_keys("NewArticleToDelete")
        article_about.click()
        article_about.send_keys("About to delete")
        article_text.click()
        article_text.send_keys("Text to delete")
        article_tags.click()
        article_tags.send_keys("Tag to delete")
        xpath(self.driver, "//html").click()
        time.sleep(2)
        article_publish_button.click()
        time.sleep(2)

        title_of_article_to_delete = xpath(self.driver, '//h1')
        print(title_of_article_to_delete.text)
        main_window = self.driver.window_handles[0]
        # ATC_08 Step 02-03: Ellenorizzuk a ’Delete article’ gomb megjeleneset, majd kattintsunk ra.
        delete_article_button = xpath(self.driver, '//button[@class = "btn btn-outline-danger btn-sm"]')
        delete_article_button.click()
        time.sleep(2)
        # ATC_08 Step 04: A torlest ellenorizzuk a torolt cikk url-jenek megadasaval es az oldalon a cim adat hianyaval.
        self.driver.execute_script("window.open('http://localhost:1667/#/articles/newarticletodelete')")
        deleted_article_window = self.driver.window_handles[1]
        self.driver.switch_to.window(deleted_article_window)
        time.sleep(2)
        deleted_article_title = xpath(self.driver, '//h1')
        assert deleted_article_title.text == ''
        self.driver.close()
        self.driver.switch_to.window(main_window)

        print("Test 8 - Deleting Article successful")

    ############################# Test 9 - Save article to document #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_09 szam alatt.
    # ATC_09 Step 01: Oldal megnyitasa + Sutik elfogadasa + Bejelentkezes + uj cikk letrehozasa.
    def test__save_to_file(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        create_new_article(self.driver)
        # ATC_09 Step 02-03: Jeloljuk ki a cikk adatait tartalmazo html elemeket es soronkent irjuk ki beloluk adatokat.
        article_title = xpath(self.driver, '//*[@id="app"]/div/div[1]/div/h1')
        article_author = xpath(self.driver, '//a[@class="author"]')
        article_text = xpath(self.driver, '//*[@id="app"]/div/div[2]/div[1]/div/div[1]/p')
        article_tag = xpath(self.driver, '//a[@class="tag-pill tag-default"]')
        article_data = [article_title, article_author, article_text, article_tag]
        with open("article_data.txt", 'w') as file_write:
            for i in range(4):
                file_write.write(article_data[i].text + '\n')
        # ATC_09 Step 04: A mentest ellenorizzuk a dokumentumba irt sorok es a weblapon levo adatok osszevetsesevel.
        with open("article_data.txt", 'r') as file_read:
            for i in range(4):
                read_lines = file_read.readline()
                assert read_lines == (article_data[i].text + '\n')
        print("Test 9 - Save article to document successful")

    ############################# Test 10 - List Articles #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_10 szam alatt.
    # ATC_10 Step 01: Oldal megnyitasa + Sutik elfogadasa + Bejelentkezes.
    def test__list_articles(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        preview_list = self.driver.find_elements_by_xpath('//a[@class="preview-link"]')
        number_of_article_previews = len(preview_list)
        number_of_articles = 0
        for article in preview_list:
            number_of_articles += 1
        assert number_of_articles == number_of_article_previews
        print("Test 10 - Listing Content successful")

    ############################# Test 11 - Pagination #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_11 szam alatt.
    # ATC_11 Step 01: Oldal megnyitasa + Sutik elfogadasa + Bejelentkezes.
    def test__pagination(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        #ATC_11 Step 02-03: Jarjuk be a kilistazott cikkek osszes oldalat.
        article_page_list = self.driver.find_elements_by_class_name("page-link")
        last_page_number = 0
        for page in article_page_list:
            page.click()
            last_page_number = int(page.text)
        assert last_page_number == len(article_page_list)

        print("Test 11 - Pagination successful!")

    ############################# Test 12 - Log out #############################
    # A teszteset megtalalhato a conduit_automated_tst_1.0 documentum ATC_12 szam alatt.
    # ATC_12 Step 01: Oldal megnyitasa + Sutik elfogadasa + Bejelentkezes.
    def test__logout(self):
        accept_cookies(self.driver)
        logging_in(self.driver)
        # ATC_12 Step 02-03: Ellenorizzuk a ’Log out’ gomb megjeleneset, majd kattintsunk ra.
        log_out_button = webwait_by_xpath(self.driver, 5, '//*[@class="nav-link" and contains(text(),"Log out")]')
        assert log_out_button.text == " Log out"
        log_out_button.click()
        # ATC_12 Step 04: A kijelentkezest ellenorizzuk a 'Sign up' gomb megjelenesevel.
        sign_up_field = webwait_by_xpath(self.driver, 10, '//a[@href="#/register"]')
        assert sign_up_field.text == "Sign up"
        print("Test 12 - Logging out successful")
