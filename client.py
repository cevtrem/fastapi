import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api():
    # Уникальные имена пользователей для тестов
    user_name = f"user_{datetime.now().timestamp()}"
    admin_name = f"admin_{datetime.now().timestamp()}"

    # 1. Создание пользователя
    print("\n1. Создание пользователя:")
    user_resp = requests.post(f"{BASE_URL}/user", json={
        "name": user_name,
        "password": "12345"
    })
    print(f"Status: {user_resp.status_code}")
    print("Response:", user_resp.json())
    user_id = user_resp.json().get("id")

    # 2. Создание администратора
    print("\n2. Создание администратора:")
    admin_resp = requests.post(f"{BASE_URL}/user", json={
        "name": admin_name,
        "password": "admin123",
        "role": "admin"
    })
    print(f"Status: {admin_resp.status_code}")
    print("Response:", admin_resp.json())
    admin_id = admin_resp.json().get("id")

    # 3. Логин пользователя
    print("\n3. Логин пользователя:")
    user_login_resp = requests.post(f"{BASE_URL}/login", json={
        "name": user_name,
        "password": "12345"
    })
    print(f"Status: {user_login_resp.status_code}")
    print("Response:", user_login_resp.json())
    user_token = user_login_resp.json().get("token")

    # 4. Логин администратора
    print("\n4. Логин администратора:")
    admin_login_resp = requests.post(f"{BASE_URL}/login", json={
        "name": admin_name,
        "password": "admin123"
    })
    print(f"Status: {admin_login_resp.status_code}")
    print("Response:", admin_login_resp.json())
    admin_token = admin_login_resp.json().get("token")

    # 5. Создание объявления пользователем
    print("\n5. Создание объявления пользователем:")
    create_data = {
        "title": "Продам iPhone 15",
        "description": "Новый, в упаковке",
        "price": 80000
    }
    create_resp = requests.post(f"{BASE_URL}/advertisement", json=create_data, headers={"x-token": user_token})
    print(f"Status: {create_resp.status_code}")
    print("Response:", create_resp.json())
    ad_id = create_resp.json().get("id")

    # 6. Получение объявления
    print("\n6. Получение объявления:")
    get_resp = requests.get(f"{BASE_URL}/advertisement/{ad_id}")
    print(f"Status: {get_resp.status_code}")
    print("Response:", get_resp.json())

    # 7. Обновление объявления пользователем
    print("\n7. Обновление объявления пользователем:")
    update_data = {
        "title": "Продам iPhone 15 Pro",
        "price": 85000
    }
    update_resp = requests.patch(f"{BASE_URL}/advertisement/{ad_id}", json=update_data, headers={"x-token": user_token})
    print(f"Status: {update_resp.status_code}")
    print("Response:", update_resp.json())

    # 8. Удаление объявления пользователем
    print("\n8. Удаление объявления пользователем:")
    delete_resp = requests.delete(f"{BASE_URL}/advertisement/{ad_id}", headers={"x-token": user_token})
    print(f"Status: {delete_resp.status_code}")
    print("Response:", delete_resp.json())

    # 9. Удаление объявления администратором
    print("\n6. Удаление объявления администратором:")
    admin_delete_ad_resp = requests.delete(f"{BASE_URL}/advertisement/{ad_id}", headers={"x-token": admin_token})
    print(f"Status: {admin_delete_ad_resp.status_code}")
    print("Response:", admin_delete_ad_resp.json())

    # 10. Проверка прав администратора на удаление пользователя
    print("\n7. Проверка прав администратора на удаление пользователя:")
    admin_delete_user_resp = requests.delete(f"{BASE_URL}/user/{user_id}", headers={"x-token": admin_token})
    print(f"Status: {admin_delete_user_resp.status_code}")
    try:
        print("Response:", admin_delete_user_resp.json())
    except Exception as e:
        print("Error decoding response:", e)

    # 11. Проверка прав неавторизованного пользователя
    print("\n8. Проверка прав неавторизованного пользователя:")
    unauth_resp = requests.get(f"{BASE_URL}/user/{admin_id}")
    print(f"Status: {unauth_resp.status_code}")
    try:
        print("Response:", unauth_resp.json())
    except Exception as e:
        print("Error decoding response:", e)


if __name__ == "__main__":
    test_api()