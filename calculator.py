import configparser
import os
import sys

def load_config():
    config = configparser.ConfigParser()
    # Используем абсолютный путь к файлу
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    # Проверяем существование файла
    if not os.path.exists(config_path):
        print(f"Ошибка: файл {config_path} не найден!")
        sys.exit(1)
    
    config.read(config_path)
    return config

def calculate_speed(base_speed, current_sens, target_sens, vertical_multiplier):
    # Новая формула для расчета скорости с учетом вертикального множителя
    # Скорость = Базовая скорость * (Целевая чувствительность / Базовая чувствительность) * (1 / Множитель вертикальной чувствительности)
    return base_speed * (target_sens / 20) * (1 / vertical_multiplier)

def update_profiles():
    config = load_config()
    
    # Текущая чувствительность в конфиге
    current_sens = float(config['Settings']['sensitivity'])
    
    # Получаем все параметры из конфига
    vertical_multiplier = float(config['Settings']['vertical_multiplier'])
    # Расчет параметров для каждого профиля
    profiles = {
        'F1': {  # Beryl
            'name': 'beryl', 
            'speed': calculate_speed(float(config['Settings']['beryl_speed']), 20, current_sens, vertical_multiplier),
            'speed_growth_rate': float(config['Settings']['beryl_speed_growth_rate'])
        },
        'F2': {  # AUG
            'name': 'aug',
            'speed': calculate_speed(float(config['Settings']['aug_speed']), 20, current_sens, vertical_multiplier),
            'speed_growth_rate': float(config['Settings']['aug_speed_growth_rate'])
        },
        'F3': {  # M4
            'name': 'm4',
            'speed': calculate_speed(float(config['Settings']['m4_speed']), 20, current_sens, vertical_multiplier),
            'speed_growth_rate': float(config['Settings']['m4_speed_growth_rate'])
        },
        'F4': {  # Mutant
            'name': 'mutant',
            'speed': calculate_speed(float(config['Settings']['mutant_speed']), 20, current_sens, vertical_multiplier),
            'speed_growth_rate': float(config['Settings']['mutant_speed_growth_rate']),
            'click_interval': float(config['Settings']['mutant_click_interval'])
        },
        'dmr': {
            'name': 'dmr',
            'speed': calculate_speed(float(config['Settings']['dmr_speed']), 20, current_sens, vertical_multiplier),
            'speed_growth_rate': 0.0
        }
    }
    
    return profiles

def main():
    profiles = update_profiles()
    print("\nТекущие параметры для ваших настроек:")
    print("-" * 50)
    for key, profile in profiles.items():
        print(f"{profile['name'].upper()}")
        print(f"  Скорость: {profile['speed']:.2f}")
        print(f"  Рост скорости (эксп): {profile['speed_growth_rate']}")
        if 'click_interval' in profile:
            print(f"  Интервал кликов: {profile['click_interval']:.3f}")
        print("-" * 50)

if __name__ == "__main__":
    main()
