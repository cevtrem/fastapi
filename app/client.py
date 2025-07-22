import requests
from datetime import datetime


BASE_URL = "http://localhost:8000"


def test_api():
    # 1. Создание объявления
    print("\n1. Создание объявления:")
    create_data = {
        "title": "Продам iPhone 15",
        "description": "Новый, в упаковке",
        "price": 80000,
        "owner": "user123",
        "created_at": datetime.now().isoformat()
    }
    create_resp = requests.post(f"{BASE_URL}/advertisement", json=create_data)
    print(f"Status: {create_resp.status_code}")
    print("Response:", create_resp.json())
    ad_id = create_resp.json().get("id")

    # 2. Получение объявления
    print("\n2. Получение объявления:")
    get_resp = requests.get(f"{BASE_URL}/advertisement/{ad_id}")
    print(f"Status: {get_resp.status_code}")
    print("Response:", get_resp.json())

    # 3. Поиск объявлений (исправленный URL)
    print("\n3. Поиск объявлений:")
    search_resp = requests.get(f"{BASE_URL}/advertisement/",
                               params={"title": "Продам iPhone 15"})
    print(f"Status: {search_resp.status_code}")
    print("Response:", search_resp.json())

    # 4. Обновление объявления (только изменяемые поля)
    print("\n4. Обновление объявления:")
    update_data = {
        "title": "Продам iPhone 15 Pro",
        "price": 85000
    }
    update_resp = requests.patch(f"{BASE_URL}/advertisement/{ad_id}",
                                 json=update_data)
    print(f"Status: {update_resp.status_code}")
    print("Response:", update_resp.json())

    # 5. Проверка обновления
    print("\n5. Проверка обновления:")
    get_resp = requests.get(f"{BASE_URL}/advertisement/{ad_id}")
    print("Updated data:", get_resp.json())

    # 6. Удаление объявления
    print("\n6. Удаление объявления:")
    delete_resp = requests.delete(f"{BASE_URL}/advertisement/{ad_id}")
    print(f"Status: {delete_resp.status_code}")
    print("Response:", delete_resp.json())

    # 7. Проверка удаления
    print("\n7. Проверка удаления:")
    get_resp = requests.get(f"{BASE_URL}/advertisement/{ad_id}")
    print(f"Status: {get_resp.status_code}")
    print("Response:", get_resp.json())


if __name__ == "__main__":
    test_api()
