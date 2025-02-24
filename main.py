import yaml
import tuyapower
from prometheus_client import start_http_server, Gauge
import time
import logging

# Настроим базовое логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Загружаем конфигурацию из YAML файла
def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.info(f"Конфигурация загружена из {config_path}")
        return config
    except Exception as e:
        logging.error(f"Ошибка загрузки конфигурации: {e}")
        raise

# Определяем метрики Prometheus
power_gauge = Gauge('tuya_smartplug_power', 'Total power used, in Watts', ['device'])
voltage_gauge = Gauge('tuya_smartplug_voltage', 'Electrical voltage, in Volts', ['device'])
current_gauge = Gauge('tuya_smartplug_current', 'Current in milliamps', ['device'])
state_gauge = Gauge('tuya_smartplug_switch_on', 'Whether the plug is switched on (1 for on, 0 for off)', ['device'])
daily_kwh_gauge = Gauge('tuya_smartplug_power_kwh_day', 'Projected power consumption in kWh per day', ['device'])

def collect_metrics(devices):
    for device in devices:
        name, device_id, key, ip, protocol = device['name'], device['id'], device['key'], device['ip'], device['protocol']
        try:
            on, w, mA, V, err = tuyapower.deviceInfo(device_id, ip, key, protocol)
            power_gauge.labels(device=name).set(w)
            voltage_gauge.labels(device=name).set(V)
            current_gauge.labels(device=name).set(mA)
            state_gauge.labels(device=name).set(1 if on else 0)

            # Проекция потребления энергии на день (в кВт·ч)
            if on:
                day = (w / 1000.0) * 24  # kWh в день
                daily_kwh_gauge.labels(device=name).set(day)

            logging.debug(f"Данные для устройства {name} обновлены")
        except Exception as e:
            logging.error(f"Ошибка получения данных с {name}: {e}")

def main():
    try:
        config = load_config('config.yaml')
        start_http_server(9155)
        logging.info("Prometheus сервер запущен на порту 9155")
        while True:
            collect_metrics(config)
            time.sleep(10)
    except Exception as e:
        logging.error(f"Ошибка запуска приложения: {e}")

if __name__ == "__main__":
    main()
