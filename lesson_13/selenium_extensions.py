"""
ДОПОЛНИТЕЛЬНЫЕ РАСШИРЕНИЯ для Selenium-кода
Файл с дополнительными классами и утилитами для еще большего улучшения
"""
import json
import csv
from enum import Enum
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging


class AlertType(Enum):
    """Типы alert'ов для лучшей типизации"""
    SIMPLE = "simple"
    TIMER = "timer"
    CONFIRM = "confirm"
    PROMPT = "prompt"


@dataclass
class TestResult:
    """Результат выполнения теста"""
    test_name: str
    status: str  # "PASSED", "FAILED", "ERROR"
    duration: float
    error_message: str = ""
    screenshot_path: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class TestReporter:
    """Класс для создания отчетов о тестировании"""
    
    def __init__(self, config):
        self.config = config
        self.results: List[TestResult] = []
        self.logger = logging.getLogger("TestReporter")
    
    def add_result(self, result: TestResult):
        """Добавить результат теста"""
        self.results.append(result)
        self.logger.info(f"Тест {result.test_name}: {result.status}")
    
    def generate_json_report(self, filename: str = "test_report.json"):
        """Генерирует JSON отчет"""
        report_data = {
            "summary": {
                "total_tests": len(self.results),
                "passed": len([r for r in self.results if r.status == "PASSED"]),
                "failed": len([r for r in self.results if r.status == "FAILED"]),
                "errors": len([r for r in self.results if r.status == "ERROR"]),
                "generated_at": datetime.now().isoformat()
            },
            "results": [asdict(result) for result in self.results]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"JSON отчет сохранен: {filename}")
    
    def generate_csv_report(self, filename: str = "test_report.csv"):
        """Генерирует CSV отчет"""
        if not self.results:
            return
        
        fieldnames = list(asdict(self.results[0]).keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for result in self.results:
                writer.writerow(asdict(result))
        
        self.logger.info(f"CSV отчет сохранен: {filename}")
    
    def print_summary(self):
        """Выводит краткую сводку результатов"""
        total = len(self.results)
        passed = len([r for r in self.results if r.status == "PASSED"])
        failed = len([r for r in self.results if r.status == "FAILED"])
        errors = len([r for r in self.results if r.status == "ERROR"])
        
        print(f"\n{'='*50}")
        print(f"СВОДКА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
        print(f"{'='*50}")
        print(f"Всего тестов: {total}")
        print(f"✅ Пройдено: {passed}")
        print(f"❌ Провалено: {failed}")
        print(f"🚫 Ошибок: {errors}")
        print(f"📊 Успешность: {(passed/total*100):.1f}%" if total > 0 else "0%")


class ConfigManager:
    """Управление конфигурациями для разных сред"""
    
    @staticmethod
    def load_from_file(config_path: str) -> Dict[str, Any]:
        """Загружает конфигурацию из JSON файла"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"Файл конфигурации {config_path} не найден")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка парсинга JSON конфигурации: {e}")
            return {}
    
    @staticmethod
    def save_config_template(filename: str = "config_template.json"):
        """Создает шаблон конфигурационного файла"""
        template = {
            "webdriver_path": "path/to/yandexdriver.exe",
            "browser_path": "path/to/browser.exe",
            "base_url": "https://demoqa.com/alerts",
            "explicit_wait": 10,
            "screenshot_dir": "screenshots",
            "window_size": [1920, 1080],
            "headless": True,
            "environments": {
                "development": {
                    "base_url": "https://dev.demoqa.com/alerts",
                    "headless": False
                },
                "staging": {
                    "base_url": "https://staging.demoqa.com/alerts",
                    "headless": True
                },
                "production": {
                    "base_url": "https://demoqa.com/alerts",
                    "headless": True
                }
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"Шаблон конфигурации создан: {filename}")


class AlertTestData:
    """Тестовые данные для alert'ов"""
    
    ALERT_TEXTS = {
        AlertType.SIMPLE: "You clicked a button",
        AlertType.TIMER: "This alert appeared after 5 seconds", 
        AlertType.CONFIRM: "Do you confirm action?",
        AlertType.PROMPT: "Please enter your name"
    }
    
    EXPECTED_RESULTS = {
        "confirm_accept": "You selected Ok",
        "confirm_dismiss": "You selected Cancel"
    }
    
    TEST_INPUTS = {
        "prompt_text": "test_text",
        "prompt_empty": "",
        "prompt_special": "Тест 123 !@#"
    }


class PerformanceMonitor:
    """Мониторинг производительности тестов"""
    
    def __init__(self):
        self.start_times = {}
        self.logger = logging.getLogger("PerformanceMonitor")
    
    def start_timing(self, test_name: str):
        """Начать измерение времени теста"""
        self.start_times[test_name] = datetime.now()
        self.logger.debug(f"Начало измерения времени для {test_name}")
    
    def end_timing(self, test_name: str) -> float:
        """Закончить измерение времени теста"""
        if test_name not in self.start_times:
            self.logger.warning(f"Время начала для {test_name} не найдено")
            return 0.0
        
        duration = (datetime.now() - self.start_times[test_name]).total_seconds()
        self.logger.info(f"Тест {test_name} выполнен за {duration:.2f} сек")
        del self.start_times[test_name]
        return duration


# Пример использования расширений
def example_usage():
    """Пример использования дополнительных классов"""
    
    # Создание шаблона конфигурации
    ConfigManager.save_config_template()
    
    # Работа с отчетами
    reporter = TestReporter(None)
    
    # Добавление результатов тестов
    reporter.add_result(TestResult("test_simple_alert", "PASSED", 2.5))
    reporter.add_result(TestResult("test_timer_alert", "PASSED", 7.1))
    reporter.add_result(TestResult("test_confirm_alert", "FAILED", 1.8, "Assertion error"))
    
    # Генерация отчетов
    reporter.generate_json_report()
    reporter.generate_csv_report()
    reporter.print_summary()
    
    # Мониторинг производительности
    perf_monitor = PerformanceMonitor()
    perf_monitor.start_timing("test_example")
    # ... выполнение теста ...
    duration = perf_monitor.end_timing("test_example")


if __name__ == "__main__":
    example_usage()
