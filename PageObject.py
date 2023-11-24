from BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class Locators_Auth:
    """"Локаторы для страницы авторизации"""
    Locator_Email_Field = (By.ID, 'loginEmail')
    Locator_Password_Field = (By.ID, 'loginPassword')
    Locator_Authorization_Button = (By.ID, 'authButton')
    Locator_Title = (By.TAG_NAME, 'h3')
    Locator_Error_Message = (By.CLASS_NAME, 'uk-alert')

class Locators_Menu:
    """"Локаторы для переключения по страницам"""
    Locator_Menu_Table = (By.ID, 'menuUsersOpener')
    Locator_Variant_Button = (By.ID, 'menuMore')
    Locator_Table_Button = (By.ID, 'menuUsersOpener')
    Locator_Add_User_Button = (By.ID, 'menuUserAdd')
    Locator_Table = (By.ID, 'menuUsers')
    Locator_Main = (By.ID, 'menuMain')

class Locators_Add_User:
    """"Локаторы для страницы добавления пользователя"""
    Locator_Email_Field = (By.ID, 'dataEmail')
    Locator_Password_Field = (By.ID, 'dataPassword')
    Locator_Name_Field = (By.ID, 'dataName')
    Locator_Gender = (By.ID, 'dataGender')
    Locator_Variant_1_1 = (By.ID, 'dataSelect11')
    Locator_Variant_1_2 = (By.ID, 'dataSelect12')
    Locator_Variant_2_1 = (By.ID, 'dataSelect21')
    Locator_Variant_2_2 = (By.ID, 'dataSelect22')
    Locator_Variant_2_3 = (By.ID, 'dataSelect23')
    Locator_Add_User_Button = (By.ID, 'dataSend')
    Locator_Message = (By.XPATH, "//div[@class='uk-modal-body']")
    Locator_Invalid_Message = (By.CLASS_NAME, 'uk-alert')
    Locator_Ok_Button = (By.XPATH, "//button[@class='uk-button uk-button-primary uk-modal-close']")
    Locator_Table = (By.ID, 'dataTable')

class Auth(BasePage):
    """Функции для авторизации"""
    def enter_email(self, word):
        search_field = self.find_element(Locators_Auth.Locator_Email_Field)
        search_field.send_keys(word)
        return search_field

    def enter_password(self, word):
        search_field = self.find_element(Locators_Auth.Locator_Password_Field)
        search_field.send_keys(word)
        return search_field

    def click_on_the_enter_button(self):
        return self.find_element(Locators_Auth.Locator_Authorization_Button, time=2).click()

    def search_title(self):
        main_title = self.find_element(Locators_Auth.Locator_Title, time=2)
        return main_title

    def search_error_message(self):
        error_message = self.find_element(Locators_Auth.Locator_Error_Message, time=2)
        return error_message

class Menu(BasePage):
    """"Функции перехода по вкладкам"""
    def click_on_the_variant_button(self):
        return self.find_element(Locators_Menu.Locator_Variant_Button, time=2).click()

    def click_on_the_table(self):
        return self.find_element(Locators_Menu.Locator_Table_Button, time=2).click()

    def click_on_the_add_user_button(self):
        return self.find_element(Locators_Menu.Locator_Add_User_Button, time=2).click()

    def click_on_the_table_button(self):
        return self.find_element(Locators_Menu.Locator_Table, time=2).click()

    def click_on_main_button(self):
        return self.find_element(Locators_Menu.Locator_Main, time=2).click()

class Add_User(BasePage):
    """Функции добавления пользователя"""
    def enter_email(self, word):
        search_field = self.find_element(Locators_Add_User.Locator_Email_Field)
        search_field.send_keys(word)
        return search_field

    def enter_password(self, word):
        search_field = self.find_element(Locators_Add_User.Locator_Password_Field)
        search_field.send_keys(word)
        return search_field

    def enter_name(self, word):
        search_field = self.find_element(Locators_Add_User.Locator_Name_Field)
        search_field.send_keys(word)
        return search_field

    def choose_gender(self):
        dropdown = self.find_element(Locators_Add_User.Locator_Gender)
        select = Select(dropdown)
        return select.select_by_visible_text("Женский")

    def click_on_button_variant_1_2(self):
        return self.find_element(Locators_Add_User.Locator_Variant_1_2, time=2).click()

    def click_on_button_variant_2_1(self):
        return self.find_element(Locators_Add_User.Locator_Variant_2_1, time=2).click()

    def click_on_button_variant_2_2(self):
        return self.find_element(Locators_Add_User.Locator_Variant_2_2, time=2).click()

    def click_on_button_variant_2_3(self):
        return self.find_element(Locators_Add_User.Locator_Variant_2_3, time=2).click()

    def click_on_add_user_button(self):
        return self.find_element(Locators_Add_User.Locator_Add_User_Button, time=2).click()

    def click_on_ok_button(self):
        return self.find_element(Locators_Add_User.Locator_Ok_Button, time=2).click()

    def search_message(self):
        return self.find_element(Locators_Add_User.Locator_Message, time=2)

    def search_error_message(self):
        return self.find_element(Locators_Add_User.Locator_Invalid_Message, time=2)

    def search_table(self):
        table = self.find_elements(Locators_Add_User.Locator_Table, time=2)
        users_string = [x.text for x in table]
        users = [s.split() for s in users_string]
        return users





