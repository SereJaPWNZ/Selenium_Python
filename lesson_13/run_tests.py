#!/usr/bin/env python3
"""
Простой запускатель тестов с выбором режима
"""
import sys
import argparse
from corrected_selenium_alerts import main, Config

def run_with_options():
    """Запуск тестов с опциями командной строки"""
    parser = argparse.ArgumentParser(description='Запуск Selenium тестов alert\'ов')
    parser.add_argument('--headless', action='store_true', help='Запуск в headless режиме')
    parser.add_argument('--visible', action='store_true', help='Запуск с видимым браузером')
    parser.add_argument('--screenshots', action='store_true', help='Включить скриншоты')
    
    args = parser.parse_args()
    
    # Настройка конфигурации на основе аргументов
    config = Config()
    
    if args.visible:
        config.headless = False
        print("🔍 Режим: Видимый браузер")
    elif args.headless:
        config.headless = True
        print("👻 Режим: Headless браузер")
    
    print(f"🎯 URL: {config.base_url}")
    print(f"⏱️ Timeout: {config.explicit_wait}s")
    print(f"📸 Скриншоты: {config.screenshot_dir}")
    
    # Запуск тестов
    return main()

if __name__ == "__main__":
    sys.exit(run_with_options())
