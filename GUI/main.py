# conda install -c conda-forge ffmpeg   # установка ffmpeg


import os
import tkinter as tk
from tkinter import filedialog, PhotoImage, Label, Text, ttk, END
import pyaudio
import wave
import json
import time
import psutil
import cProfile
import pstats
from classifier import classif
from Trancribator import Trancribator

# Запись с микрофона
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"
JSON_FILE_PATH = r"submission.json"

# Инициализация PyAudio
p = pyaudio.PyAudio()


def start_recording():
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()

    # Сохранение записанного аудио
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # После записи обработаем файл
    process_audio(WAVE_OUTPUT_FILENAME)


# Функция для поиска данных в JSON
def найти_в_json(audio_filepath):
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                if item.get("audio_filepath") == audio_filepath:
                    return item.get("audio_filepath"), item.get("text"), item.get("label"), item.get("attribute")
    except FileNotFoundError:
        return None
    return None


# Функция выбора файла
def выбрать_файл():
    file_path = filedialog.askopenfilename(filetypes=[("Аудио файлы", "*.mp3;*.wav")])
    if file_path:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.mp3', '.wav']:
            process_audio(file_path)
        else:
            text.delete(1.0, END)
            text.insert(END, "Неверный формат файла. Выберите файл MP3 или WAV.")


# Обработка аудио файла
def process_audio(audio_file):
    trn = Trancribator()
    clf = classif()

    st = time.time()

    # Получаем текст и метки
    text_value = trn.predict(audio_file)
    text_value = sanitize_text(text_value).lstrip()
    label, attribute = clf.predict(text_value)
    elapsed_time = time.time() - st

    # Обновляем текстовое поле результатами
    text.delete(1.0, END)
    text.insert(END, f"Audio Filepath: {audio_file}\n")
    text.insert(END, f"Text: {text_value}\n")
    text.insert(END, f"Label: {label}\n")
    text.insert(END, f"Attribute: {attribute}\n")

    # Добавляем данные в JSON
    save_to_json(audio_file, text_value, label, attribute)

    # Получаем информацию о CPU и памяти
    memory_usage, cpu_usage = get_memory_and_cpu_usage()
    print(f"Использование памяти (RSS): {memory_usage / (1024 ** 2):.2f} MB")
    print(f"Использование CPU: {cpu_usage:.2f}%")


def sanitize_text(text):
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='ignore')
    return text


def save_to_json(audio_file, text_value, label, attribute):
    data = {
        "audio_filepath": os.path.basename(audio_file),
        "text": text_value,
        "label": int(label),
        "attribute": int(attribute)
    }

    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, ensure_ascii=False, indent=4)
    else:
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([data], file, ensure_ascii=False, indent=4)


def get_memory_and_cpu_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    cpu_usage = process.cpu_percent(interval=0.1)
    return memory_info.rss, cpu_usage


# Интерфейс
root = tk.Tk()
root.title("Audio Processor")
root.geometry("1280x720")
root.resizable(width=False, height=False)

# bg
bg = PhotoImage(file="HD.png")
my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

# Лого
logo = PhotoImage(file="logo.png")
rjd_logo = Label(root, image=logo, height=100, width=100)
rjd_logo.grid(row=0, column=1, padx=[0, 0])

# Надпись
main_label = Label(root, text='Вставьте .mp3 .wav файл \n или начните запись голоса', font=("Arial", 30, 'bold'),
                   fg="black")
main_label.grid(row=0, column=2, padx=[200, 200])

# Кнопка выбора файла
btn = ttk.Button(root, text="Выбрать аудио...", command=выбрать_файл)
btn.place(relx=0.5, rely=0.3, anchor="c", width=180, height=40)

# Кнопка начала записи
button = tk.Button(root, text="Начать запись", command=start_recording)
button.place(relx=0.5, rely=0.2, anchor="c", width=180, height=40)

# Текстовое поле
text = Text(root, height=10, width=60)
text.place(relx=0.5, rely=0.5, anchor="c", width=360, height=180)

root.mainloop()