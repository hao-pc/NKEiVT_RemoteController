# from classifier import classif  
# from Trancribator import Trancribator
# import json
# import time
# import os 


# def sanitize_text(text):
#     # Проверяем, что текст действительно является строкой
#     if isinstance(text, bytes):
#         # Если текст в байтах, декодируем его
#         text = text.decode('utf-8', errors='ignore')
    
#     # Здесь можно добавить другие методы обработки текста, если необходимо
#     return text

# def main():
#     trn = Trancribator()
#     clf = classif()

#     st = time.time()
#     audio_file = r"inference\2d6f5040-76fe-11ee-b168-c09bf4619c03.mp3"
    
#     # Получаем текст и метки
#     text = trn.predict(audio_file)
#     print(f"Raw text from prediction: {text}")  # Печатаем полученный текст для отладки
#     text = sanitize_text(text).lstrip()  # Обработка текста и удаление пробелов слева
#     label, attribute = clf.predict(text)
#     elapsed_time = time.time() - st

#     # print('Время исполнения:', elapsed_time, 'секунд')
#     # print(f"Текст: {text}, Класс: {label}, Атрибюте: {attribute}")

#     # Создаем или обновляем JSON-файл
#     json_file = "submission.json"
    
#     # Преобразуем label и attribute в стандартные типы Python
#     data = {
#         "audio_filepath": os.path.basename(audio_file),
#         "text": text,
#         "label": int(label),  # Преобразуем в int
#         "attribute": int(attribute)  # Преобразуем в int
#     }

#     # Проверяем, существует ли файл
#     if os.path.exists(json_file):
#         # Если файл существует, добавляем данные
#         with open(json_file, "r+", encoding="utf-8") as file:  # Указываем кодировку UTF-8
#             file_data = json.load(file)  # Загружаем существующие данные
#             file_data.append(data)  # Добавляем новые данные
#             file.seek(0)  # Перемещаем указатель в начало файла
#             json.dump(file_data, file, ensure_ascii=False, indent=4)  # Сохраняем обновленный список
#     else:
#         # Если файл не существует, создаем его и записываем данные
#         with open(json_file, "w", encoding="utf-8") as file:  # Указываем кодировку UTF-8
#             json.dump([data], file, ensure_ascii=False, indent=4)  # Записываем данные в формате списка

# if __name__ == "__main__":
#     main()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# from classifier import classif  
# from Trancribator import Trancribator
# import json
# import time
# import os 
# import cProfile
# import pstats

# def sanitize_text(text):
#     # Проверяем, что текст действительно является строкой
#     if isinstance(text, bytes):
#         # Если текст в байтах, декодируем его
#         text = text.decode('utf-8', errors='ignore')
    
#     # Здесь можно добавить другие методы обработки текста, если необходимо
#     return text

# def main():
#     trn = Trancribator()
#     clf = classif()

#     st = time.time()
#     audio_file = r"inference\2d6f5040-76fe-11ee-b168-c09bf4619c03.mp3"
    
#     # Получаем текст и метки
#     text = trn.predict(audio_file)
#     print(f"Raw text from prediction: {text}")  # Печатаем полученный текст для отладки
#     text = sanitize_text(text).lstrip()  # Обработка текста и удаление пробелов слева
#     label, attribute = clf.predict(text)
#     elapsed_time = time.time() - st

#     # print('Время исполнения:', elapsed_time, 'секунд')
#     # print(f"Текст: {text}, Класс: {label}, Атрибюте: {attribute}")

#     # Создаем или обновляем JSON-файл
#     json_file = "submission.json"
    
#     # Преобразуем label и attribute в стандартные типы Python
#     data = {
#         "audio_filepath": os.path.basename(audio_file),
#         "text": text,
#         "label": int(label),  # Преобразуем в int
#         "attribute": int(attribute)  # Преобразуем в int
#     }

#     # Проверяем, существует ли файл
#     if os.path.exists(json_file):
#         # Если файл существует, добавляем данные
#         with open(json_file, "r+", encoding="utf-8") as file:  # Указываем кодировку UTF-8
#             file_data = json.load(file)  # Загружаем существующие данные
#             file_data.append(data)  # Добавляем новые данные
#             file.seek(0)  # Перемещаем указатель в начало файла
#             json.dump(file_data, file, ensure_ascii=False, indent=4)  # Сохраняем обновленный список
#     else:
#         # Если файл не существует, создаем его и записываем данные
#         with open(json_file, "w", encoding="utf-8") as file:  # Указываем кодировку UTF-8
#             json.dump([data], file, ensure_ascii=False, indent=4)  # Записываем данные в формате списка

# if __name__ == "__main__":
#     # Профилирование кода и запись в файл
#     profiler = cProfile.Profile()
#     profiler.enable()  # Начинаем профилирование
#     main()  # Запускаем основную функцию
#     profiler.disable()  # Останавливаем профилирование

#     # Записываем результаты профилирования в файл
#     with open("cProfile_code.txt", "w") as f:
#         stats = pstats.Stats(profiler, stream=f)
#         stats.strip_dirs()  # Убираем лишние директории из путей
#         stats.sort_stats('cumulative')  # Сортируем по времени
#         stats.print_stats()  # Печатаем статистику в файл











from classifier import classif  
from Trancribator import Trancribator
import json
import time
import os 
import cProfile
import pstats
import psutil

def sanitize_text(text):
    # Проверяем, что текст действительно является строкой
    if isinstance(text, bytes):
        # Если текст в байтах, декодируем его
        text = text.decode('utf-8', errors='ignore')
    
    return text

def get_memory_and_cpu_usage():
    # Получаем информацию о процессе
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    cpu_usage = process.cpu_percent(interval=0.1)  # 0.1 секунда для получения среднего значения
    
    return memory_info.rss, cpu_usage  # Возвращаем использованную память и загрузку ЦП

def main():
    trn = Trancribator()
    clf = classif()

    st = time.time()
    audio_file = "2d6f5040-76fe-11ee-b168-c09bf4619c03.mp3"
    
    # Получаем текст и метки
    text = trn.predict(audio_file)
    print(f"Raw text from prediction: {text}")  # Печатаем полученный текст для отладки
    text = sanitize_text(text).lstrip()  # Обработка текста и удаление пробелов слева
    label, attribute = clf.predict(text)
    elapsed_time = time.time() - st

    # print('Время исполнения:', elapsed_time, 'секунд')
    # print(f"Текст: {text}, Класс: {label}, Атрибюте: {attribute}")

    # Создаем или обновляем JSON-файл
    json_file = "submission.json"
    
    # Преобразуем label и attribute в стандартные типы Python
    data = {
        "audio_filepath": os.path.basename(audio_file),
        "text": text,
        "label": int(label),  # Преобразуем в int
        "attribute": int(attribute)  # Преобразуем в int
    }

    # Проверяем, существует ли файл
    if os.path.exists(json_file):
        # Если файл существует, добавляем данные
        with open(json_file, "r+", encoding="utf-8") as file:  # Указываем кодировку UTF-8
            file_data = json.load(file)  # Загружаем существующие данные
            file_data.append(data)  # Добавляем новые данные
            file.seek(0)  # Перемещаем указатель в начало файла
            json.dump(file_data, file, ensure_ascii=False, indent=4)  # Сохраняем обновленный список
    else:
        # Если файл не существует, создаем его и записываем данные
        with open(json_file, "w", encoding="utf-8") as file:  # Указываем кодировку UTF-8
            json.dump([data], file, ensure_ascii=False, indent=4)  # Записываем данные в формате списка

if __name__ == "__main__":
    # Профилирование кода и запись в файл
    profiler = cProfile.Profile()
    profiler.enable()  # Начинаем профилирование
    main()  # Запускаем основную функцию
    profiler.disable()  # Останавливаем профилирование

    # Получаем информацию о CPU и памяти
    memory_usage, cpu_usage = get_memory_and_cpu_usage()

    # Записываем результаты профилирования в файл
    with open("cProfile_code.txt", "w", encoding="utf-8") as f:  # Указываем кодировку UTF-8
        f.write(f"Использование памяти (RSS): {memory_usage / (1024 ** 2):.2f} MB\n")  # Память в МБ
        f.write(f"Использование CPU: {cpu_usage:.2f}%\n\n")  # CPU в процентах
        
        stats = pstats.Stats(profiler, stream=f)
        stats.strip_dirs()  # Убираем лишние директории из путей
        stats.sort_stats('cumulative')  # Сортируем по времени
        stats.print_stats()  # Печатаем статистику в файл

