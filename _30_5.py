import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_all_pets():
    pytest.driver = webdriver.Chrome(r'C:/Users/_01/Desktop/SkillFactory/chromedriver.exe')
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # ввод email
    email = pytest.driver.find_element(by=By.ID, value="email")
    email.send_keys("m_s2000@mail.ru")
    # ввод пароля
    password = pytest.driver.find_element(by=By.ID, value="pass")
    password.send_keys("Gress789")
    # неявное ожидание
    pytest.driver.implicitly_wait(3)
    # входим в акк
    btn_submit = pytest.driver.find_element(by=By.XPATH, value="//button[@type='submit']")
    btn_submit.click()
    # проверка страницы
    assert pytest.driver.find_element(by=By.TAG_NAME, value='a').text == "PetFriends"

    images = pytest.driver.find_elements(by=By.CSS_SELECTOR, value='div#all_my_pets > table > tbody > tr > th > img')
    names = pytest.driver.find_elements(by=By.CSS_SELECTOR, value='div#all_my_pets > table > tbody > tr > td')
    descriptions = pytest.driver.find_elements(by=By.CSS_SELECTOR, value='div#all_my_pets > table > tbody > tr > '
                                                                         'td:nth-of-type(2)')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

    pytest.driver.quit()


def test_show_my_pets():
    pytest.driver = webdriver.Chrome(r'C:/Users/_01/Desktop/SkillFactory/chromedriver.exe')
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # ввод email
    email = pytest.driver.find_element(by=By.ID, value="email")
    email.send_keys("m_s2000@mail.ru")
    # ввод пароля
    password = pytest.driver.find_element(by=By.ID, value="pass")
    password.send_keys("Gress789")
    # неявное ожидание
    pytest.driver.implicitly_wait(3)
    # входим в акк
    btn_submit = pytest.driver.find_element(by=By.XPATH, value="//button[@type='submit']")
    btn_submit.click()
    # переходим в каталог моих питомцев
    my_pets = pytest.driver.find_element(by=By.PARTIAL_LINK_TEXT, value="Мои питомцы")
    my_pets.click()
    # проверка страницы
    assert pytest.driver.find_element(by=By.TAG_NAME, value='a').text == "PetFriends"

    # Ищем в теле таблицы все строки с полными данными питомцев
    data_my_pets = pytest.driver.find_elements(by=By.CSS_SELECTOR, value='tbody>tr')

    # Ожидаем, что данные всех питомцев видны на странице
    for i in range(len(data_my_pets)):
        assert WebDriverWait(pytest.driver, 3).until(EC.visibility_of(data_my_pets[i]))

    # Ищем в теле таблицы все фотографии питомцев и ожидаем, что все загруженные фото, видны на странице
    image_my_pets = pytest.driver.find_elements(by=By.CSS_SELECTOR, value='img[style="max-width: 100px; max-height: '
                                                                          '100px;"]')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert WebDriverWait(pytest.driver, 3).until(EC.visibility_of(image_my_pets[i]))

    # Ищем в теле таблицы все имена питомцев и ожидаем увидеть их на странице
    name_my_pets = pytest.driver.find_elements(by=By.XPATH, value='//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert WebDriverWait(pytest.driver, 3).until(EC.visibility_of(name_my_pets[i]))

    # Ищем в теле таблицы все породы питомцев и ожидаем увидеть их на странице
    type_my_pets = pytest.driver.find_elements(by=By.XPATH, value='//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert WebDriverWait(pytest.driver, 3).until(EC.visibility_of(type_my_pets[i]))

    # Ищем в теле таблицы все данные возраста питомцев и ожидаем увидеть их на странице
    age_my_pets = pytest.driver.find_elements(by=By.XPATH, value='//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert WebDriverWait(pytest.driver, 3).until(EC.visibility_of(age_my_pets[i]))

    # Ищем на странице всю статистику пользователя и проверяем соответствие статистики
    user_stat = pytest.driver.find_element(by=By.XPATH, value='//div[@class=".col-sm-4 left"]').text.split("\n")
    stat_pets = user_stat[1].split(" ")
    all_my_pets = int(stat_pets[-1])
    assert len(data_my_pets) == all_my_pets

    # Проверяем, что хотя бы у половины питомцев есть фото
    m = 0
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            m += 1
    assert m >= all_my_pets / 2

    # Проверяем, что у всех питомцев есть имя
    for i in range(len(name_my_pets)):
        assert name_my_pets[i].text != ''

    # Проверяем, что у всех питомцев есть порода
    for i in range(len(type_my_pets)):
        assert type_my_pets[i].text != ''

    # Проверяем, что у всех питомцев есть возраст
    for i in range(len(age_my_pets)):
        assert age_my_pets[i].text != ''

    # Проверяем, что в списке нет повторяющихся питомцев:
    list_data_my_pets = []
    for i in range(len(data_my_pets)):
        list_data = data_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
        list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список
    set_data_my_pets = set(list_data_my_pets)  # преобразовываем список в множество
    assert len(list_data_my_pets) == len(
        set_data_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть

    pytest.driver.quit()
