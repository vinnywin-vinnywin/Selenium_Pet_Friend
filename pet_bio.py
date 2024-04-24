"""
#тестируемый сайт: petfriends.skillfactory.ru
#массовый поиск элементов - проверка всех питомцев пользователя на наличие имени, вида и возраста
#адрес драйвера: D:\SF_Start29\03_AutoPy\Example_test_text\distr
#каждый раз для запуска тестов необходимо указать, какой именно браузер мы хотим использовать:
pytest -v --driver Chrome --driver-path D:/SF_Start29/03_AutoPy/Example_test_text/distr/chromedriver.exe
#для запуска в терминале PyCharme:
python -m pytest -v --driver Chrome --driver-path D:/SF_Start29/03_AutoPy/Example_test_text/distr/chromedriver.exe tests/pet_bio.py
"""

import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
# Для пользователей Windows
chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5) #вставить ожидание
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver

    driver.quit()

test_debug = 0 #переменная для отображения отладочных комментариев, 0-нет комментов, 1-есть

def test_show_all_pets(driver):
    if test_debug == 1: print("\n----------------------------we are in test_show_all_pets - START") #
    WDW(driver, 5).until(EC.presence_of_element_located((By.ID, 'email'))) #вставить ожидание
    driver.find_element(By.ID, 'email').send_keys('vinnywin@yandex.ru') # Вводим email
    driver.find_element(By.ID, 'pass').send_keys('123Test!123') # Вводим пароль
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click() # Нажимаем на кнопку входа в аккаунт
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    if test_debug == 1: print("----------------------------we are in test_show_all_pets - in my_pet-page") #

    # список всех обьектов питомца , в котром есть атрибут ".text" с помощью которого,
    # можно получить информацию о питомце в виде строки: 'Мурзик Котэ 5'
    WDW(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/td[1]"))) #вставить ожидание
    all_my_pets = driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/td[1]")
    if test_debug == 1: print("----------------------------we are in test_show_all_pets - all_my_pets")  #

    # этот список image объектов , который имееют метод get_attribute('src') ,
    # благодаря которому можно посмотреть есть ли изображение питомца или нет.
    #all_pets_images = driver.find_elements(By.XPATH, '//[@id="all_my_pets"]/table[1]/tbody/tr/th/img') #-
    all_pets_images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/th/img')
    if test_debug == 1: print("----------------------------we are in test_show_all_pets - all_pets_images")  #

    # проверяем что список своих питомцев не пуст
    if test_debug == 1: print("----------------------------we are in test_show_all_pets - проверка список !=0")  #
    assert len(all_my_pets) > 0

    pets_info_list = []
    for i in range(len(all_my_pets)):
        if test_debug == 1: print("----------------------------we are in test_show_all_pets - вошли в цикл")  #
        pets_info = all_my_pets[i].text.split("\n") #отделяем от данных питомца
        pets_info_list.append(pets_info[0]) #выбираем эл-т и добавляем его в список
        set_my_pets = set(pets_info) #преобразуем список в множество
        assert len(pets_info_list) == len(set_my_pets) #сравниваем длину списка и множ-ва - без повторов должн совпадать

    if test_debug == 1: print("количество питомцев ", len(all_my_pets)+1, "\n----------------------------we are in test_show_all_pets - END") #счет с 0 переводим в счет с 1



def test_pets_have_name_age_breed(driver):
#У всех питомцев есть имя, возраст и порода
    if test_debug == 1: print("\n----------------------------we are in test_pets_have_name_age_breed - START") #
    driver.find_element(By.ID, 'email').send_keys('vinnywin@yandex.ru') # Вводим email
    driver.find_element(By.ID, 'pass').send_keys('123Test!123') # Вводим пароль
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click() # Нажимаем на кнопку входа в аккаунт
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - in my_pet-page") #

    #список объектов питомцев с атрибутом text
    #my_pets = driver.find_elements(By.XPATH, "//*[@id='my_pets']/table/tbody") #/tr[1]/td[1]
    #my_pets = driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody")
    my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')


    # проверяем наличие изображения
    my_pets_img = driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/th") # //*[@id="all_my_pets"]/table/tbody/tr[1]/th/img
    for i in range(len(my_pets_img)):
        assert my_pets_img[i].get_attribute('src') != ''
    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - images")  #
    # проверяем наличие имени
    my_pets_name = driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/td[1]") #//*[@id="all_my_pets"]/table/tbody/tr[1]/td[1]
    for i in range(len(my_pets_name)):
        assert my_pets_name[i].text != ''
    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - name")  #
    # проверяем возраст
    my_pets_age = driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/td[2]")
    for i in range(len(my_pets_age)):
        assert my_pets_age[i].text != ''
    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - age")  #
    # проверяем породу
    my_pets_breed = driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/td[3]")
    for i in range(len(my_pets_breed)):
        assert my_pets_breed[i].text != ''
    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - breed")  #


    #проверяем, что список не пуст
    assert len(my_pets) > 0
    pets_info = []
    for i in range(len(my_pets)):
        pets_info = my_pets[i].text #получаем информацию из списка питомцев
        pets_info = pets_info.split("\n")[0] #избавляемся от лишних символов
        pets_info.join(pets_info) #добавляем информацию про иня, возраст, породу
    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - pets_info not empty")  #

    #проверяем, что у питомцев разные имена
    pets_name_my_pets = []
    for i in range(len(my_pets_name)):
        pets_name_my_pets.append(my_pets_name[i].text)
    set_name_my_pets = set(pets_name_my_pets)
    assert len(pets_name_my_pets) == len(set_name_my_pets)
    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - diferent name")  #

    #проверяем, что в списаке нет повторяющихся элементов
    pets_info_my_pets = []
    for i in range(len(my_pets)):
        pets_info = my_pets[i].text.split("\n")
        pets_info_my_pets.append(pets_info[0])
    set_info_my_pets = set(pets_info_my_pets)
    assert len (pets_info_my_pets) == len(set_info_my_pets)
    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - pet is unique")  #

    if test_debug == 1: print("----------------------------we are in test_pets_have_name_age_breed - END")  #







