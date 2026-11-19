import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_saucedemo_add_to_cart():
    # 1. Налаштування Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--guest")

    # Якщо тест запущено на GitHub Actions — вмикаємо режим без графічного вікна
    if os.getenv("GITHUB_ACTIONS") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # 2. Відкриття тестового сайту
        print("Переходимо на сайт SauceDemo...")
        driver.get("https://www.saucedemo.com/")

        # 3. Введення логіна та пароля
        print("Вводимо облікові дані...")
        username_field = wait.until(EC.element_to_be_clickable((By.ID, "user-name")))
        username_field.send_keys("standard_user")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")

        # 4. Натискання кнопки Вхід
        print("Натискаємо кнопку Login...")
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # 5. Перевірка успішної авторизації
        print("Перевіряємо перехід у каталог...")
        title_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))
        assert title_element.text == "Products", f"Очікували 'Products', але отримали '{title_element.text}'"

        # 6. Додавання товару (Sauce Labs Backpack) у кошик
        print("Додаємо товар у кошик...")
        add_to_cart_button = wait.until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        add_to_cart_button.click()

        # 7. Перевірка лічильника товарів на іконці кошика
        print("Перевіряємо лічильник кошика...")
        cart_badge = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        assert cart_badge.text == "1", f"Очікували '1' у кошику, але отримали '{cart_badge.text}'"

        print("РЕЗУЛЬТАТ: Тест успішно пройдено (PASSED)!")

    except Exception as error:
        print(f"РЕЗУЛЬТАТ: Тест впав з помилкою: {error}")
        raise error

    finally:
        # 8. Закриття браузера
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    test_saucedemo_add_to_cart()