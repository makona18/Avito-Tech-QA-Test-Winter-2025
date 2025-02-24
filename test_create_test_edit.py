import pytest
from playwright.sync_api import sync_playwright, Page

BASE_URL = "http://tech-avito-intern.jumpingcrab.com/"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
    page.close()


# Функция для создания объявления
def create_ad(page: Page, name: str, price: str, description: str, image_url: str):
    page.click("text=Создать")
    page.fill("input[name='name']", name)
    page.fill("input[name='price']", price)
    page.fill("input[name='description']", description)
    page.fill("input[name='imageUrl']", image_url)
    page.click("text=Сохранить")
    page.wait_for_load_state("networkidle")


# Функция для поиска объявления
def search_ad(page: Page, name: str):
    page.fill("input[placeholder='Поиск по объявлениям']", name)
    page.click("text=Найти")
    page.wait_for_load_state("networkidle")


# Тест на создание объявления

def test_create_ad(page):
    name, price, description, image_url = "Фотография великолепного кота", "2056", "Это Линус! Здесь вы можете посмотреть на него за деньги. Погладить его в ирл - бесценно", "https://sun9-66.userapi.com/impg/YDwmC4PhROAhzhTWMzU-UXSENXeNkEOI2s-lOw/XtsHYIk02Sg.jpg?size=960x1280&quality=95&sign=45e14229f6b0c492fc0aa705826b88c8&type=album"
    create_ad(page, name, price, description, image_url)
    search_ad(page, name)

    assert page.locator(f"img[src='{image_url}']").is_visible(), "Изображение не найдено"
    assert page.locator("text=" + name).is_visible(), "Название объявления не найдено"
    assert page.locator("text=" + price).is_visible(), "Цена объявления не найдена"
    assert page.locator("text=" + description).is_visible(), "Описание объявления не найдено"


# Тест на редактирование объявления

def test_edit_ad(page):
    new_name, new_price, new_description, new_image_url = "Тест", "900", "Отредактирован", "https://avatars.mds.yandex.net/i?id=742a91fcbbedb351a7598f81d2eb7259_l-12569575-images-thumbs&n=13"
    page.click("svg[style='cursor: pointer;']")

    page.fill("input[name='name']", new_name)
    page.fill("input[name='price']", new_price)
    page.fill("input[name='description']", new_description)
    page.fill("input[name='imageUrl']", new_image_url)
    page.click("svg[style='cursor: pointer;']")
    page.wait_for_load_state("networkidle")

    assert page.locator(f"img[src='{new_image_url}']").is_visible(), "Новое изображение не найдено"
    assert page.locator("text=" + new_name).is_visible(), "Название объявления не обновлено"
    assert page.locator("text=" + new_price).is_visible(), "Цена объявления не обновлена"
    assert page.locator("text=" + new_description).is_visible(), "Описание объявления не обновлено"
