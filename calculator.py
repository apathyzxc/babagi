import configparser
import os

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
    
    # Базовые значения для sens 20
    beryl_base = float(config['Settings']['beryl_speed'])
    aug_base = float(config['Settings']['aug_speed'])
    m4_base = float(config['Settings']['m4_speed'])
    mutant_base = float(config['Settings']['mutant_speed'])
    dmr_base = float(config['Settings']['dmr_speed'])
    
    # Получаем все параметры из конфига
    vertical_multiplier = float(config['Settings']['vertical_multiplier'])
    
    # Расчет параметров для каждого профиля
    profiles = {
        'F1': {  # Beryl
            'name': 'beryl', 
            'speed': calculate_speed(float(config['Settings']['beryl_speed']), 20, current_sens, vertical_multiplier),
            'normal_speed_increase': float(config['Settings']['beryl_normal_speed_increase']),
            'normal_increase_time': float(config['Settings']['beryl_normal_increase_time'])
        },
        'F2': {  # AUG
            'name': 'aug',
            'speed': calculate_speed(float(config['Settings']['aug_speed']), 20, current_sens, vertical_multiplier),
            'normal_speed_increase': float(config['Settings']['aug_normal_speed_increase']),
            'normal_increase_time': float(config['Settings']['aug_normal_increase_time'])
        },
        'F3': {  # M4
            'name': 'm4',
            'speed': calculate_speed(float(config['Settings']['m4_speed']), 20, current_sens, vertical_multiplier),
            'normal_speed_increase': float(config['Settings']['m4_normal_speed_increase']),
            'normal_increase_time': float(config['Settings']['m4_normal_increase_time'])
        },
        'F4': {  # Mutant
            'name': 'mutant',
            'speed': calculate_speed(float(config['Settings']['mutant_speed']), 20, current_sens, vertical_multiplier),
            'normal_speed_increase': float(config['Settings']['mutant_normal_speed_increase']),
            'normal_increase_time': float(config['Settings']['mutant_normal_increase_time']),
            'click_interval': float(config['Settings']['mutant_click_interval'])
        },
        'dmr': {
            'name': 'dmr',
            'speed': calculate_speed(float(config['Settings']['dmr_speed']), 20, current_sens, vertical_multiplier),
            'normal_speed_increase': float(config['Settings']['dmr_normal_speed_increase']),
            'normal_increase_time': float(config['Settings']['dmr_normal_increase_time'])
        }
    }
    
    return profiles
    
    return {
        'F1': {  # Beryl
            'name': 'beryl', 
            'speed': beryl_speed,
            'normal_speed_increase': 10.5,
            'normal_increase_time': 0.7
        },
        'F2': {  # AUG
            'name': 'aug',
            'speed': aug_speed,
            'normal_speed_increase': 11.35,
            'normal_increase_time': 1.25
        },
        'F3': {  # M4
            'name': 'm4',
            'speed': m4_speed,
            'normal_speed_increase': 2.65,
            'normal_increase_time': 0.5
        },
        'F4': {  # Mutant
            'name': 'mutant',
            'speed': mutant_speed,
            'normal_speed_increase': 9.35,
            'normal_increase_time': 1.25,
            'click_interval': 0.01
        },
        'dmr': {
            'name': 'dmr',
            'speed': dmr_speed,
            'normal_speed_increase': 0.0,
            'normal_increase_time': 0.0
        }
    }

def main():
    profiles = update_profiles()
    print("\nТекущие параметры для ваших настроек:")
    print("-" * 50)
    for key, profile in profiles.items():
        print(f"{profile['name'].upper()}")
        print(f"  Скорость: {profile['speed']:.2f}")
        print(f"  Увеличение скорости: {profile['normal_speed_increase']}")
        print(f"  Время увеличения: {profile['normal_increase_time']:.2f}")
        if 'click_interval' in profile:
            print(f"  Интервал кликов: {profile['click_interval']:.3f}")
        print("-" * 50)

if __name__ == "__main__":
    main()
