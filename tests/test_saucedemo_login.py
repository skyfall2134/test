import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGIN_URL = "https://www.saucedemo.com"
USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
LOGIN_BTN = (By.ID, "login-button")
ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")
INVENTORY_ITEM_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img")


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")  # comment out to run with visible browser
    options.add_argument("--window-size=1280,720")

    driver = webdriver.Chrome(service=ChromeService(), options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def login(driver, username: str, password: str):
    driver.get(LOGIN_URL)
    driver.find_element(*USERNAME).clear()
    driver.find_element(*USERNAME).send_keys(username)
    driver.find_element(*PASSWORD).clear()
    driver.find_element(*PASSWORD).send_keys(password)
    driver.find_element(*LOGIN_BTN).click()


def wait_for_error(driver):
    return WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(ERROR_CONTAINER)
    )


def test_standard_user_can_login(driver):
    login(driver, "standard_user", "secret_sauce")
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url


def test_locked_out_user_is_blocked(driver):
    login(driver, "locked_out_user", "secret_sauce")
    err = wait_for_error(driver)
    assert "locked out" in err.text.lower()


def test_wrong_password_shows_error(driver):
    login(driver, "standard_user", "wrong_password")
    err = wait_for_error(driver)
    assert "username and password do not match" in err.text.lower()


def test_empty_fields_show_validation(driver):
    login(driver, "", "")
    err = wait_for_error(driver)
    assert "username is required" in err.text.lower()


def test_problem_user_has_broken_images(driver):
    login(driver, "problem_user", "secret_sauce")
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))

    images = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(INVENTORY_ITEM_IMAGES)
    )
    broken_images = [
        img for img in images if "sl-404" in (img.get_attribute("src") or "")
    ]

    assert broken_images, "Expected at least one broken image for problem_user"

