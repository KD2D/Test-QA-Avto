import json
import os


def log_result(sellerId, response, item_id):
    log_file = "tests.json"

    # Создаём
    log_new = {
        "sellerId": sellerId,
        "status_code": response.status_code,
        "url": response.url,
        "error": response.text if response.status_code != 200 else "None",
        "item_id": item_id
    }


    # Читаем
    logs = []
    try:
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
    except:
        logs = []

    logs.append(log_new)

    # Сохраняем обратно в файл
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)
