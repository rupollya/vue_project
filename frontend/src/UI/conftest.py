import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import time
from selenium.webdriver import ActionChains

connection = pymysql.connect(
                user='root',
                password='505750',
                host='localhost',
                port=3306,
                database='task_manager3'
            )

link = "http://localhost:5173"


@pytest.fixture(scope="function")
def browser():
    print("\nstart chrome browser for test..")
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    yield browser
    print("\nquit browser..")
    browser.quit()

@pytest.fixture(scope="function")
def authlog(browser):
    browser.get(link)
    login_input = browser.find_element(By.ID, "login")
    login_input.send_keys('testuser')
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys('123qQ!')
    browser.find_element(By.CSS_SELECTOR, ".btn.btn-light.w-100").click()
    
    
@pytest.fixture(scope="module")
def account_preparation():
    try:
        browser = webdriver.Chrome()
        browser.get(link)
        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys('testuser')
        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys('123qQ!')
        browser.find_element(By.CSS_SELECTOR, ".btn.btn-light.w-100").click()
        browser.quit()
        return browser
    except:
        browser = webdriver.Chrome()
        browser.implicitly_wait(10)

        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth").click()
        # Если пользователь не существует, то мы создаем нового
        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys('testuser')
        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys('123qQ!')
        browser.find_element(By.CSS_SELECTOR, ".btn.btn-light.w-100").click()

        # Ждем, пока пользователь создастся
        WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
        
        browser = webdriver.Chrome()
        browser.implicitly_wait(10)
        browser.get(link)
        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys('testuser')
        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys('123qQ!')
        browser.find_element(By.CSS_SELECTOR, ".btn.btn-light.w-100").click()
        WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
        

        # Заполняем поля формы
        title_input = browser.find_element(By.ID, "nametask")
        title_input.send_keys("Новая задача")
        deadline_input = browser.find_element(By.ID, "date")
        deadline_input.send_keys("2024-07-27")
        importance_select = browser.find_element(By.CSS_SELECTOR, "select.form-select")
        importance_select.send_keys("Высокая")

        # Нажимаем кнопку "Добавить задачу"
        browser.find_element(By.CSS_SELECTOR, ".btn.btn-secondary").click()
        WebDriverWait(browser, 10).until(EC.url_contains("tasks"))

        return browser
    
    

