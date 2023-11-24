import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from PageObject import Auth
from PageObject import Menu
from PageObject import Add_User
import random
import string
from faker import Faker


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.close()

if __name__ == '__main__':
    pytest.main()
def authorization(driver):
    authtorization_page = Auth(driver)
    authtorization_page.go_to_site()
    driver.maximize_window()
    authtorization_page.enter_email('test@protei.ru')
    authtorization_page.enter_password('test')
    authtorization_page.click_on_the_enter_button()

"""Тесты авторизации"""
def test_auth_positiv(driver):
    authtorization_page = Auth(driver)
    authtorization_page.go_to_site()
    authtorization_page.enter_email('test@protei.ru')
    authtorization_page.enter_password('test')
    authtorization_page.click_on_the_enter_button()
    main_title = authtorization_page.search_title()
    assert main_title.is_displayed()
    assert main_title.get_attribute('class') == 'uk-card-title'
    assert main_title.text == 'Добро пожаловать!'

def test_auth_negativ_invalid_password(driver):
    authtorization_page = Auth(driver)
    authtorization_page.go_to_site()
    authtorization_page.enter_email('test@protei.ru')
    authtorization_page.enter_password('12345')
    authtorization_page.click_on_the_enter_button()
    error_message = authtorization_page.search_error_message()
    assert error_message.get_attribute('class') == 'uk-alert uk-alert-danger'
    assert error_message.text == ('Неверный E-Mail или пароль')

def test_auth_negativ_invalid_email(driver):
    authtorization_page = Auth(driver)
    authtorization_page.go_to_site()
    authtorization_page.enter_email('12345@protei.ru')
    authtorization_page.enter_password('test')
    authtorization_page.click_on_the_enter_button()
    error_message = authtorization_page.search_error_message()
    assert error_message.get_attribute('class') == 'uk-alert uk-alert-danger'
    assert error_message.text == ('Неверный E-Mail или пароль' )

def test_auth_negativ_incorrect_email_1(driver):
    authorization_page = Auth(driver)
    authorization_page.go_to_site()
    authorization_page.enter_email('12345')
    authorization_page.enter_password('test')
    authorization_page.click_on_the_enter_button()
    error_message = authorization_page.search_error_message()
    assert error_message.get_attribute('class') == 'uk-alert uk-alert-danger'
    assert  error_message.text == ('Неверный формат E-Mail')

def test_auth_negativ_incorrect_email_2(driver):
    authorization_page = Auth(driver)
    authorization_page.go_to_site()
    authorization_page.enter_email('@protei.ru')
    authorization_page.enter_password('test')
    authorization_page.click_on_the_enter_button()
    error_message = authorization_page.search_error_message()
    assert error_message.get_attribute('class') == 'uk-alert uk-alert-danger'
    assert error_message.text == ('Неверный формат E-Mail')

def test_auth_negativ_incorrect_email_3(driver):
    authorization_page = Auth(driver)
    authorization_page.go_to_site()
    authorization_page.enter_email('12345@')
    authorization_page.enter_password('test')
    authorization_page.click_on_the_enter_button()
    error_message = authorization_page.search_error_message()
    assert error_message.get_attribute('class') == 'uk-alert uk-alert-danger'
    assert error_message.text == ('Неверный формат E-Mail')

"""Тест страницы с вариантами"""
def test_check_variant(driver):
    authorization(driver)
    variant_page = Menu(driver)
    variant_page.click_on_the_variant_button()
    variant_page = Auth(driver)
    title = variant_page.search_title()
    assert title.is_displayed()
    assert title.get_attribute('class') == 'uk-card-title'
    assert title.text == 'НТЦ ПРОТЕЙ'

"""Тесты добавления пользователей"""
def test_add_positive_user(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('12345')
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if name in user:
            flag = True
    assert flag == True

"""Тесты с паролем"""
def test_add_user_password_1000_symbols(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=1000))
    add_user.enter_password(password)
    add_user.enter_name('Bob1245')
    add_user.click_on_add_user_button()
    error_message = add_user.search_message()
    assert error_message.text == ('ОШИБКА! undefined')

def test_add_user_password_1_symbols_and_different_variant(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=1))
    add_user.enter_password(password)
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_name(name)
    add_user.click_on_button_variant_1_2()
    add_user.click_on_button_variant_2_3()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if name in user:
            flag = True
    assert flag == True

def test_add_user_empty_password_(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('')
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_button_variant_2_1()
    add_user.click_on_add_user_button()
    error_message = add_user.search_error_message()
    assert error_message.text == 'Поле Пароль не может быть пустым'

def test_add_user_password_with_spaces(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))
    add_user.enter_password(password + '     ' + password)
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_name(name)
    add_user.click_on_button_variant_1_2()
    add_user.click_on_button_variant_2_3()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if name in user:
            flag = True
    assert flag == True

"""Тесты с именем"""
def test_add_user_name_1000_symbols(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('123456')
    name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=1000))
    add_user.enter_name(name)
    add_user.click_on_add_user_button()
    error_message = add_user.search_message()
    assert error_message.text == ('ОШИБКА! FAIL')

def test_add_user_name_30_symbols_and_without_variant_2(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('123456')
    name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=30))
    add_user.enter_name(name)
    add_user.click_on_button_variant_2_1()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if name in user:
            flag = True
    assert flag == True

def test_add_user_name_with_XSS_injection(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('123456')
    fake = Faker('ru_Ru')
    name = fake.first_name() + '<script>alert(123)</script>'
    add_user.enter_name(name )
    add_user.click_on_button_variant_2_1()
    add_user.click_on_add_user_button()
    error_message = add_user.search_message()
    assert error_message.text == ('ОШИБКА! FAIL')

def test_add_user_empty_name(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
    add_user.enter_password(password)
    add_user.enter_name('')
    add_user.click_on_button_variant_2_3()
    add_user.click_on_add_user_button()
    error_message = add_user.search_error_message()
    assert error_message.text == 'Поле Имя не может быть пустым'

def test_add_user_name_with_special_symbol(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('123456')
    fake = Faker('ru_Ru')
    name = fake.first_name() + '__+_))_+_?!~@'
    add_user.enter_name(name)
    add_user.click_on_button_variant_2_1()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if name in user:
            flag = True
    assert flag == True

def test_add_user_name_with_spaces(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('123456')
    name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))
    add_user.enter_name(name + '    ' + name)
    add_user.choose_gender()
    add_user.click_on_button_variant_2_3()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if name in user:
            flag = True
    assert flag == True

def test_add_user_with_japan_name(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('12345')
    fake = Faker('jp_JP')
    name = fake.first_name()
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_button_variant_2_1()
    add_user.click_on_button_variant_2_2()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if name in user:
            flag = True
    assert flag == True

def test_add_user_full_name(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email('Иван@0987654321')
    add_user.enter_password('12345')
    fake = Faker('ru_Ru')
    name = fake.name()
    add_user.enter_name(name)
    name = name.split()
    add_user.choose_gender()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for n in name:
        for user in users:
            if n in user:
                flag = True
            else:
                flag = False
    assert flag == True

"""Тесты с email"""
def test_add_user_email_with_invalid_mail_1(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_email(name + '@')
    add_user.enter_password('12345')
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_add_user_button()
    error_message = add_user.search_error_message()
    assert error_message.text == 'Неверный формат E-Mail'

def test_add_user_email_with_invalid_mail_2(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_email('@protei.ru')
    add_user.enter_password('12345')
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_add_user_button()
    error_message = add_user.search_error_message()
    assert error_message.text == 'Неверный формат E-Mail'

def test_add_user_email_with_invalid_mail_3(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_email(name)
    add_user.enter_password('12345')
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_add_user_button()
    error_message = add_user.search_error_message()
    assert error_message.text == 'Неверный формат E-Mail'

def test_add_user_email_with_1_symbol(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    email = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=1)) + '@protei.ru'
    add_user.enter_email(email)
    add_user.enter_password('123456')
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_button_variant_2_3()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()
    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if email in user:
            flag = True
    assert flag == True

def test_add_user_with_large_email(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    email = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=150)) + '@protei.ru'
    add_user.enter_email(email)
    add_user.enter_password('123456')
    fake = Faker('ru_Ru')
    name = fake.first_name()
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_button_variant_2_3()
    add_user.click_on_add_user_button()
    error_message = add_user.search_message()
    assert error_message.text == ('ОШИБКА! FAIL')

def test_add_two_users_at_the_same_time(driver):
    authorization(driver)
    page_add = Menu(driver)
    fake = Faker('ru_Ru')
    name = fake.first_name()
    email = fake.ascii_free_email()
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email(email)
    add_user.enter_password('12345')
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()

    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    add_user.enter_email(email)
    add_user.enter_password('12345')
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_add_user_button()
    message_new_user = add_user.search_message()
    assert message_new_user.text == 'Данные добавлены.'
    add_user.click_on_ok_button()

    page_add.click_on_the_table()
    page_add.click_on_the_table_button()
    users = add_user.search_table()
    flag = False
    for user in users:
        if name in user:
            flag = True
    assert flag == True

"""Тест перехода на главную страницу после добавления пользователя"""
def test_main_page_after_add_user(driver):
    authorization(driver)
    page_add = Menu(driver)
    page_add.click_on_the_table()
    page_add.click_on_the_add_user_button()
    add_user = Add_User(driver)
    fake = Faker('ru_Ru')
    name = fake.first_name()
    email = fake.ascii_free_email()
    add_user.enter_email(email)
    add_user.enter_password('12345')
    add_user.enter_name(name)
    add_user.choose_gender()
    add_user.click_on_add_user_button()
    add_user.click_on_ok_button()
    page_add.click_on_main_button()
    add_user = Auth(driver)
    main_title = add_user.search_title()
    assert main_title.is_displayed()
    assert main_title.get_attribute('class') == 'uk-card-title'
    assert main_title.text == 'Добро пожаловать!'

