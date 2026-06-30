import os
import subprocess

# Папки где искать файлы (добавляй свои)

SEARCH_DIRS = [
    os.path.expanduser("~\\Desktop"),
    os.path.expanduser("~\\Downloads"),
    os.path.expanduser("~\\Documents"),
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    r"D:\cteam\steamapps\common",  # ← вот так
]


def find_file(name: str) -> str | None:
    """Ищет файл по имени в папках из SEARCH_DIRS"""
    for directory in SEARCH_DIRS:
        if not os.path.exists(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower() == name.lower():
                    return os.path.join(root, file)
    return None


def open_file(name: str) -> str:
    """Открыть файл по имени — путь писать не нужно"""
    path = find_file(name)
    if path is None:
        return f"❌ Файл не найден: {name}"
    try:
        os.startfile(path)
        return f"✅ Открываю: {path}"
    except Exception as e:
        return f"❌ Ошибка: {e}"