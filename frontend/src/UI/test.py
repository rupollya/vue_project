from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time


link = "http://localhost:5173"

@pytest.mark.registration
class TestRegistration():

    def test_registration_form_visibility(self, browser):
        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth")
        toggle_form_button.click()
        
        login_input = browser.find_element(By.ID, "login")
        password_input = browser.find_element(By.ID, "password")
        registration_button = browser.find_element(By.ID, "regauthbutton")
        login_input.send_keys("testuser")
        password_input.send_keys("123qQ!")
        registration_button.click()

    def test_registration_invalid_login(self, browser):
        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth")
        toggle_form_button.click()

        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys("123")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Нельзя использовать только цифры"
        
    def test_registration_invalid_login2(self, browser):
        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth")
        toggle_form_button.click()

        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys(" ")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Заполните поле!"
        
    def test_registration_invalid_password(self, browser):
        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth")
        toggle_form_button.click()

        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys("testuser")

        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys("123")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Минимум 6 символов"
        
    def test_registration_invalid_password2(self, browser):
        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth")
        toggle_form_button.click()

        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys("testuser")

        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys("123q!!")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Нужна хотя бы одна заглавная буква"
    
    def test_registration_invalid_password3(self, browser):
        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth")
        toggle_form_button.click()

        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys("testuser")

        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys("123QQ!")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Нужна хотя бы одна строчная буква"

    def test_registration_invalid_password4(self, browser):
        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth")
        toggle_form_button.click()

        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys("testuser")

        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys("123QQq")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Нужен хотя бы один специальный символ"

    def test_registration_invalid_password5(self, browser):
        browser.get(link)
        toggle_form_button = browser.find_element(By.ID, "backforth")
        toggle_form_button.click()

        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys("testuser")

        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys(" ")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Заполните поле!"

@pytest.mark.auth
class TestAuth():
    def test_auth_form_visibility(self, browser):
        browser.get(link)        
        login_input = browser.find_element(By.ID, "login")
        password_input = browser.find_element(By.ID, "password")
        registration_button = browser.find_element(By.ID, "regauthbutton")
        login_input.send_keys("testuser")
        password_input.send_keys("123qQ!")
        registration_button.click()

    def test_auth_invalid_login(self, browser):
        browser.get(link)
        
        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys(" ")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Введите логин"
        
    def test_auth_invalid_password(self, browser):
        browser.get(link)
        login_input = browser.find_element(By.ID, "login")
        login_input.send_keys("testuser")

        password_input = browser.find_element(By.ID, "password")
        password_input.send_keys(" ")

        registration_button = browser.find_element(By.ID, "regauthbutton")

        # Проверяем, что кнопка регистрации не активна
        assert not registration_button.is_enabled()

        time.sleep(1)
        error_message = browser.find_element(By.CSS_SELECTOR, ".error-message")
        assert error_message.is_displayed()
        assert error_message.text == "Введите пароль"
     
@pytest.mark.task
@pytest.mark.usefixtures("authlog")
class TestTask():
    def test_add_task(self,browser):
    # Нахождение элементов формы
        
        title_input = browser.find_element(By.ID, "nametask")
        deadline_input = browser.find_element(By.ID, "date")
        importance_select = browser.find_element(By.CSS_SELECTOR, ".form-select")
        submit_button = browser.find_element(By.CSS_SELECTOR, ".btn.btn-secondary.w-100")

        # Заполнение формы
        title_input.send_keys("Новая задача")
        deadline_input.send_keys("Дата не выбрана")
        importance_select.send_keys("Средняя")
        # Отправка формы
        submit_button.click()
        time.sleep(2)

    def test_task_visibility(self, browser):
        # Тест 1: Проверка отображения задачи
        #     Открыть страницу с задачами
        #     Проверить, что задача отображается на странице
        #     Проверить, что в задаче отображается название, срок и статус
        task_title = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task h5"))
        )
        task_deadline = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task p:nth-child(2)"))
        )
        task_status = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task p:nth-child(3)"))
        )
        assert task_title.text == "Новая задача", f"Ожидаемый текст: 'Новая задача', но получен: {task_title.text}"
        assert task_deadline.text == "Срок: Дата не выбрана", f"Срок: Дата не выбрана, но получен: {task_deadline.text}"
        assert task_status.text == "Статус: Не завершена", f"Ожидаемый текст: 'Статус: Не завершена', но получен: {task_status.text}"

        # Проверка наличия задачи на странице
        assert len(browser.find_elements(By.CSS_SELECTOR, ".task")) > 0, "Задача не найдена на странице"
    
    def test_task_status_toggle(self, browser):
        # Тест 2: Проверка переключения статуса задачи
        #     Открыть страницу с задачами
        #     Нажать кнопку "Отметить как завершённую"
        #     Проверить, что статус задачи изменился на "Завершена"
        #     Нажать кнопку "Отметить как незавершённую"
        #     Проверить, что статус задачи изменился на "Не завершена"
        # Нахождение элементов страницы
        toggle_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task button.btn-outline-light"))
        )
        status_element = browser.find_element(By.CSS_SELECTOR, ".task p:nth-child(3)")
        # Нажать кнопку "Отметить как завершённую"
        toggle_button.click()
        # Ожидание изменения статуса
        WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".task p:nth-child(3)"), "Статус: Завершена")
        )
        # Проверить, что статус задачи изменился на "Завершена"
        assert status_element.text == "Статус: Завершена", f"Ожидаемый статус: 'Статус: Завершена', фактический статус: {status_element.text}"
        # Нажать кнопку "Отметить как незавершённую"
        toggle_button.click()
        # Ожидание изменения статуса
        WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".task p:nth-child(3)"), "Статус: Не завершена")
        )
        # Проверить, что статус задачи изменился на "Не завершена"
        assert status_element.text == "Статус: Не завершена", f"Ожидаемый статус: 'Статус: Не завершена', фактический статус: {status_element.text}"
    
    
    def test_task_deletion(self, browser):
        # Тест 3: Проверка удаления задачи

        #     Открыть страницу с задачами
        #     Нажать кнопку "Удалить"
        #     Проверить, что задача исчезла со страницы
        delete_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task:first-child button.btn-danger"))
        )
        delete_button.click()
        return


     
