import win32api
import win32con
import random
from time import sleep, time
import pyttsx3
from threading import Thread
import ctypes
from ctypes import wintypes
import sys
import os
import math
from colorama import init, Fore, Back, Style
import psutil

# Инициализация colorama
init()

# Установка высокого приоритета процесса
def set_high_priority():
    try:
        process = psutil.Process(os.getpid())
        process.nice(psutil.HIGH_PRIORITY_CLASS)  # Windows
    except:
        pass  # Игнорируем ошибки если не удалось установить приоритет

# Функция очистки консоли
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Функция отображения статуса
def display_status():
    clear_console()
    print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}           Made By Namik           {Fore.CYAN}   ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════╣{Style.RESET_ALL}")
    
    # Профиль и V статус
    profile_name = profiles.get(current_profile, default_profile)['name']
    v_status = "Off" if not is_v_active else "On"
    print(f"{Fore.CYAN}║{Style.RESET_ALL} Profile: {Fore.GREEN}{profile_name:<16}{Style.RESET_ALL} {Fore.CYAN}           ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} V: {Fore.RED}{v_status:<24}{Style.RESET_ALL} {Fore.CYAN}         ║{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}╠══════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} F1-F4: Profiles   1,2: Quick switch {Fore.CYAN} ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} V: x1.5          C,Shift: +Speed    {Fore.CYAN} ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL} Insert: Update settings          {Fore.CYAN} ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")

# Настройка синтезаора речи

engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.setProperty('volume', 0.25)

# Профили оружия
def load_profiles():
    import sys
    import os
    # Добавляем директорию скрипта в путь поиска модулей
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    from calculator import update_profiles
    return update_profiles()

profiles = load_profiles()

# Профиль по умолчанию
default_profile = {'name': 'No profile', 'speed': 0.0}

# Параметры управления скоростью
shift_speed_increase = 1.5
capslock_speed_multiplier = 1.5
ctrl_speed_multiplier = 1.5

# Глобальные переменные состояния
is_v_active = False
current_profile = 'None'
last_click_time = 0
click_interval = 0.155  # DMR интервал
lmb_pressed_time = None
rmb_press_time = 0
lmb_press_time = 0
button_press_threshold = 0.05

# Классификация оружия
weapon_types = {
    'F1': 'auto',
    'F2': 'auto',
    'F3': 'auto',
    'F4': 'auto',  # Меняем 'burst' на 'auto' для правильной работы переключения
    'dmr': 'dmr'
}

# Добавим глобальную переменную для хранения последнего активного прфиля автомата
last_auto_profile = 'None'

# Добавим отслеживание начала стрельбы
spray_start_time = None

# Добавим паттерны горизонтальной отдачи для каждого оружия
recoil_patterns = {
    'F1': {  # Beryl
        'pattern': [
            (0.2, 0.3),   # Первые выстрелы немного вправо
            (0.3, 0.4),
            (0.4, 0.3),
            (-0.3, -0.4), # Затем влево
            (-0.4, -0.5),
            (-0.3, -0.4),
            (0.2, 0.3),   # И снова вправо
        ],
        'loop_pattern': True  # Зацикливать ли паттерн
    },
    'F2': {  # AUG
        'pattern': [
            (0.1, 0.2),
            (0.2, 0.3),
            (-0.2, -0.3),
            (-0.1, -0.2),
        ],
        'loop_pattern': True
    },
    # ... другие оружия ...
}

# Добавим отслеживание текущей позиции в паттерне
pattern_position = 0
spray_start_time = None

def speak(text):
    try:
        engine.endLoop()
    except:
        pass
    
    def speak_thread():
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    
    Thread(target=speak_thread).start()

def move_mouse_vertically_down(speed):
    if speed > 0:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, int(speed), 0, 0)

def calculate_saturating_speed(base_speed, elapsed_time, growth_rate, max_increase):
    if growth_rate <= 0 or max_increase <= 0:
        return base_speed
    capped_time = max(0.0, elapsed_time)
    return base_speed + max_increase * (1 - math.exp(-growth_rate * capped_time))

# Изменим функцию toggle_profile
def toggle_profile(key, profile_key):
    global current_profile, last_auto_profile
    if win32api.GetAsyncKeyState(key):
        if current_profile == profile_key:
            current_profile = 'None'
            speak("No profile")
        else:
            current_profile = profile_key
            speak(profiles[current_profile]['name'])
            if weapon_types[profile_key] == 'auto':
                last_auto_profile = profile_key
        display_status()  # Обновляем отображение
        sleep(0.2)

def handle_v_key():
    global is_v_active
    if win32api.GetAsyncKeyState(ord('V')):
        is_v_active = not is_v_active  # Переключаем состояние
        if is_v_active:
            speak("No attachments")
        else:
            speak("With attachments")
        display_status()  # Обновляем отображение
        sleep(0.2)  # Задержка для предотвращения повторного срабатывания

# Функция обновления профилей
def update_profiles_from_config():
    global profiles
    from calculator import update_profiles
    profiles = update_profiles()
    display_status()

# Добавим функции для быстрого переключения
def handle_quick_switch():
    global current_profile, last_auto_profile
    
    # Клавиша 1 - переключение на последний автомат
    if win32api.GetAsyncKeyState(ord('1')):
        if last_auto_profile != 'None' and current_profile != last_auto_profile:
            current_profile = last_auto_profile
            speak(profiles[current_profile]['name'])
            display_status()
            sleep(0.2)
    
    # Клавиша 2 - переключение на DMR
    elif win32api.GetAsyncKeyState(ord('2')):
        if current_profile != 'dmr':
            current_profile = 'dmr'
            speak('dmr')
            display_status()
            sleep(0.2)
    
    # Клавиша Insert - обновление настроек
    elif win32api.GetAsyncKeyState(win32con.VK_F12):
        update_profiles_from_config()
        sleep(0.2)

def handle_recoil_pattern(profile_key, current_time):
    global pattern_position, spray_start_time
    
    if spray_start_time is None:
        spray_start_time = current_time
        pattern_position = 0
    
    pattern_data = recoil_patterns.get(profile_key)
    if not pattern_data:
        return 0
    
    pattern = pattern_data['pattern']
    if not pattern:
        return 0
    
    # Получаем текущее значение из паттерна
    min_value, max_value = pattern[pattern_position]
    horizontal_value = random.uniform(min_value, max_value)
    
    # Обновляем позицию в паттерне
    pattern_position = (pattern_position + 1) % len(pattern) if pattern_data['loop_pattern'] else min(pattern_position + 1, len(pattern) - 1)
    
    return horizontal_value

def handle_dmr_shooting(profile):
    global last_click_time, lmb_pressed_time
    current_time = time()
    
    # Инициализация времени начала стрельбы
    if lmb_pressed_time is None:
        lmb_pressed_time = current_time
    
    return

def handle_burst_shooting(profile):
    global last_click_time, lmb_pressed_time
    current_time = time()
    
    # Автоклик с минимальным интервалом
    if current_time - last_click_time >= 0.09:  # Уменьшили интервал до 90мс
        # Быстрый клик
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        last_click_time = current_time
    
    # Инициализация времени начала стрельбы
    if lmb_pressed_time is None:
        lmb_pressed_time = current_time
    
    elapsed_time = current_time - lmb_pressed_time
    speed = calculate_saturating_speed(
        profile['speed'],
        elapsed_time,
        profile['speed_growth_rate'],
        profile['max_speed_increase']
    )
    extra_speed = 0.0
    if win32api.GetAsyncKeyState(ord('C')):
        extra_speed += calculate_saturating_speed(
            0.0,
            elapsed_time,
            profile['c_speed_growth_rate'],
            profile['c_max_speed_increase']
        )
    speed += extra_speed
    
    if win32api.GetAsyncKeyState(win32con.VK_SHIFT):
        speed += shift_speed_increase

    if win32api.GetAsyncKeyState(win32con.VK_CAPITAL):
        speed /= capslock_speed_multiplier

    if is_v_active:
        speed *= ctrl_speed_multiplier
        
    move_mouse_vertically_down(speed)

try:
    clear_console()
    display_status()
    while True:
        # Обработка профилей
        toggle_profile(win32con.VK_F1, 'F1')
        toggle_profile(win32con.VK_F2, 'F2')
        toggle_profile(win32con.VK_F3, 'F3')
        toggle_profile(win32con.VK_F4, 'F4')

        # Добавляем отключение профилей на кнопку 5
        if win32api.GetAsyncKeyState(ord('5')):
            current_profile = 'None'
            speak('off')
            display_status()
            sleep(0.2)

        handle_quick_switch()
        handle_v_key()

        # Основная логика работы с мышью
        if current_profile != 'None' and win32api.GetAsyncKeyState(win32con.VK_LBUTTON) and win32api.GetAsyncKeyState(win32con.VK_RBUTTON):
            current_time = time()
            
            if weapon_types.get(current_profile) == 'dmr':
                handle_dmr_shooting(profiles[current_profile])
            elif current_profile == 'F4':  # Mutant
                handle_burst_shooting(profiles[current_profile])
            else:
                # Логика для автоматов (F1-F3)
                if lmb_pressed_time is None:
                    lmb_pressed_time = current_time
                
                elapsed_time = current_time - lmb_pressed_time
                speed = calculate_saturating_speed(
                    profiles[current_profile]['speed'],
                    elapsed_time,
                    profiles[current_profile]['speed_growth_rate'],
                    profiles[current_profile]['max_speed_increase']
                )
                extra_speed = 0.0
                if win32api.GetAsyncKeyState(ord('C')):
                    extra_speed += calculate_saturating_speed(
                        0.0,
                        elapsed_time,
                        profiles[current_profile]['c_speed_growth_rate'],
                        profiles[current_profile]['c_max_speed_increase']
                    )
                speed += extra_speed
                
                if win32api.GetAsyncKeyState(win32con.VK_SHIFT):
                    speed += shift_speed_increase

                if win32api.GetAsyncKeyState(win32con.VK_CAPITAL):
                    speed /= capslock_speed_multiplier

                if is_v_active:
                    speed *= ctrl_speed_multiplier
                    
                move_mouse_vertically_down(speed)
        else:
            # Кнопки не зажаты вместе — сбрасываем таймеры удержания
            lmb_pressed_time = None
            last_click_time = 0

        sleep(0.001)

except KeyboardInterrupt:
    # При выходе гарантированно отпускаем ЛКМ
    print(f"\n{Fore.YELLOW}Program finished{Style.RESET_ALL}")
    sys.exit(0)
except Exception as e:
    print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
    sys.exit(1)
finally:
    try:
        engine.stop()
    except:
        pass
