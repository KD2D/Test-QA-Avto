##############################
# КОД СОЗДАН ДЛЯ ЗАДАНИЯ 2.1 #
##############################


import requests
#from random import randint
from log_tests import log_result
url = "https://qa-internship.avito.com"
#expected_status = 200

#sellerId = randint(111111, 999999)

# --- ПОЗИТИВНЫЕ СЦЕНАРИИ ---

def test_create_object():
    """Создаём объявления"""
    sellerId = 111111
    payload = {
        "sellerId": sellerId,
        "name": "Книга",
        "price": 1000,
        "statistics": {
            "likes": 100,
            "viewCount": 10000,
            "contacts": 100
        },
    }

    response = requests.post(url=f"{url}/api/1/item", json=payload)

    item_id = response.json().get("status").split()[-1]
    log_result(sellerId, response, item_id)

    print(item_id)

    assert response.status_code == 200


def test_get_object():
    """Получаем объявления по его идентификатору"""
    id_item = "Книга"
    response = requests.get(url=f"{url}/api/1/item/{id_item}")

    assert response.status_code == 200

    print(response.status_code)
    print(response.text)

def test_get_sellerId():
    """Получаем все объявления по идентификатору продавца"""
    response = requests.get(url=f"{url}/api/1/seller/{111111}/item")
    print(f"Все товары продавца {111111}: {response.json()}")
    assert response.status_code == 200

def test_check_id():
    """Получаем статистику по айтем id"""
    payload = {
        "sellerId": 111111,
        "name": "Книга",
        "price": 100,
        "statistics": {
            "likes": 10,
            "viewCount": 10,
            "contacts": 10
        },
    }

    response_post = requests.post(f"{url}/api/1/item", json=payload)
    item_id = response_post.json().get("status").split()[-1]

    # получаем его по id
    response = requests.get(f"{url}/api/1/item/{item_id}")

    print(response.json())
    assert response.status_code == 200


def test_e2e():
    """End too End"""
    # Создаём объявления
    id_item = "Книга"
    sellerId = 222222
    payload = {
        "sellerId": sellerId,
        "name": id_item,
        "price": 1000,
        "statistics": {
            "likes": 100,
            "viewCount": 10000,
            "contacts": 100
        },
    }

    response = requests.post(url=f"{url}/api/1/item", json=payload)
    item_id = response.json().get("status").split()[-1]
    print("Это в e2e", item_id)
    log_result(sellerId, response, item_id)
    assert response.status_code == 200

    # Получаем объявления по его идентификатору
    response = requests.post(url=f"{url}/api/1/item/{id_item}")
    assert response.status_code == 200

    # Получаем все объявления по идентификатору продавца
    response = requests.get(url=f"{url}/api/1/seller/{sellerId}/item")
    print(f"Все товары продавца {sellerId}: {response.json()}")
    assert response.status_code == 200

    # Получаем статистику по айтем id
    requests.get(f"{url}/api/1/item/{item_id}")
    print(f"Данные айтема: {response.json()}")
    assert response.status_code == 200

# --- НЕГАТИВНЫЕ СЦЕНАРИИ ---
def test_create_item_with_empty():
    """Проверка на пустое поле name"""
    payload = {
        "name": "",
        "price": 100,
        "sellerId": 333333
    }

    response = requests.post(url=f"{url}/api/1/item", json=payload)
    assert response.status_code != 200, "Сервер позволил создать объявление без имени!"


def test_create_item_sql_injection():
    """Проверка на SQL-инъекцию в поле name"""
    payload = {
        "name": "achoo' OR 1=1;--",
        "price": 500,
        "sellerId": 444444
    }

    response = requests.post(f"{url}/api/1/item", json=payload)
    assert response.status_code == 200, "Сервер уязвим к SQL-инъекции!"

def test_create_item_extreme_price():
    """Проверка очень большой цены"""
    payload = {
        "name": "Космический корабль",
        "price": 999999999,  # Очень большое число
        "sellerId": 555555
    }
    response = requests.post(f"{url}/api/1/item", json=payload)
    assert response.status_code == 200  # Переварит ли сервер такой масштаб


def test_create_query_idempotency():
    """Проверка идемпотентности запросов"""
    sellerId = 666666
    payload = {
        "sellerId": sellerId,
        "name": "Книга",
        "price": 5,
        "statistics": {
            "likes": 100,
            "viewCount": 100,
            "contacts": 100
        },
    }
    response = requests.post(url=f"{url}/api/1/item", json=payload)
    assert response.status_code == 200
    response = requests.post(url=f"{url}/api/1/item", json=payload)
    assert response.status_code == 200
    response = requests.post(url=f"{url}/api/1/item", json=payload)
    assert response.status_code == 200
    response = requests.post(url=f"{url}/api/1/item", json=payload)
    assert response.status_code == 200


def test_create_item_negative_val():
    """Проверка на отрицательные числа в contacts, viewCount, likes, price"""
    sellerId = 777777
    payload = {
        "sellerId": sellerId,
        "name": "Книга",
        "price": -1,
        "statistics": {
            "likes": -1,
            "viewCount": -1,
            "contacts": -1
        },
    }

    response = requests.post(url=f"{url}/api/1/item", json=payload)
    assert response.status_code != 200, "Сервер позволил создать объявление с отрицательным числом "

#create_object()
#get_object()
#get_sellerId()
#check_id()
