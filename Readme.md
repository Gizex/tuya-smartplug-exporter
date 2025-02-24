# Tuya Smart Plug Metrics Exporter

Этот проект экспортирует метрики для устройств Tuya Smart Plug в формат Prometheus. Он собирает данные о мощности, напряжении, токе, состоянии устройства и проектирует потребление энергии на день в киловатт-часах (kWh). Данные экспортируются через HTTP сервер, который Prometheus может использовать для сбора метрик.

## Описание

- **Метрики**:
  - `tuya_smartplug_power`: Общая потребляемая мощность в ваттах.
  - `tuya_smartplug_voltage`: Электрическое напряжение в вольтах.
  - `tuya_smartplug_current`: Ток в миллиамперах.
  - `tuya_smartplug_switch_on`: Состояние устройства (включено или выключено).
  - `tuya_smartplug_power_kwh_day`: Проекция потребления энергии в киловатт-часах на день.

- **Формат**: Prometheus Gauge
- **Сервер**: HTTP сервер, работающий на порту 9155, доступен для сбора метрик.

## Требования

- Python 3.7+
- Библиотеки:
  - `yaml` для работы с конфигурацией.
  - `tuyapower` для взаимодействия с устройствами Tuya.
  - `prometheus_client` для экспорта метрик в Prometheus.
  - `logging` для логирования событий.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/gizex/tuya-smartplug-exporter.git
   cd tuya-smartplug-exporter
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Убедитесь, что у вас есть доступ к устройства Tuya и получите необходимые данные (ID устройства, ключ API и IP).

4. Создайте файл конфигурации `config.yaml` с настройками для ваших устройств:

   ```yaml
   - name: "socket-2-prxmx-2"
     id: "device_id"
     key: "device_key"
     ip: "192.168.1.100"
     protocol: "v1.3"
   ```

   Укажите информацию для каждого устройства Tuya, с которым вы хотите работать.

## Запуск

Для запуска экспортера выполните следующую команду:

```bash
python tuya_exporter.py
```

Сервер будет работать на порту `9155`. Prometheus сможет собирать метрики с этого адреса:

```
http://<your-server-ip>:9155/metrics
```

## Логирование

Экспортер использует базовое логирование:

- **INFO**: Старт сервера, успешная загрузка конфигурации и обновление метрик.
- **ERROR**: Ошибки при загрузке конфигурации или получении данных от устройств.
- **DEBUG**: Обновление данных для каждого устройства.

Вы можете настроить уровень логирования, изменив `logging.basicConfig(level=logging.INFO)` в коде.

## Пример метрик

Пример метрики для мощности:

```
# HELP tuya_smartplug_power Total power used, in Watts
# TYPE tuya_smartplug_power gauge
tuya_smartplug_power{device="socket-2-prxmx-2"} 76.1
tuya_smartplug_power{device="socket-4-prxmx-1"} 19.9
# HELP tuya_smartplug_voltage Electrical voltage, in Volts
# TYPE tuya_smartplug_voltage gauge
tuya_smartplug_voltage{device="socket-2-prxmx-2"} 223.5
tuya_smartplug_voltage{device="socket-4-prxmx-1"} 229.5
# HELP tuya_smartplug_current Current in milliamps
# TYPE tuya_smartplug_current gauge
tuya_smartplug_current{device="socket-2-prxmx-2"} 414.0
tuya_smartplug_current{device="socket-4-prxmx-1"} 101.0
# HELP tuya_smartplug_switch_on Whether the plug is switched on (1 for on, 0 for off)
# TYPE tuya_smartplug_switch_on gauge
tuya_smartplug_switch_on{device="socket-2-prxmx-2"} 1.0
tuya_smartplug_switch_on{device="socket-4-prxmx-1"} 1.0
# HELP tuya_smartplug_power_kwh_day Projected power consumption in kWh per day
# TYPE tuya_smartplug_power_kwh_day gauge
tuya_smartplug_power_kwh_day{device="socket-2-prxmx-2"} 1.8264
tuya_smartplug_power_kwh_day{device="socket-4-prxmx-1"} 0.4775999999999999
```

## Автор

**Gizex** (https://github.com/gizex)

## Лицензия

Этот проект лицензирован под MIT.