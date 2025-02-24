# Tuya SmartPlug Exporter

Этот проект — это экспортер для интеграции с Prometheus, который позволяет собирать метрики с умных розеток Tuya, используя их API. Экспортер собирает информацию о мощности, токе, напряжении и состоянии устройства, а также рассчитывает проекцию потребления энергии в кВт·ч за сутки.

## Установка

### 1. С использованием Docker

Самый простой способ запустить экспортёр — это использовать Docker. Мы предоставляем готовый образ, который можно загрузить с Docker Hub.

#### Запуск с использованием Docker

1. **Запуск контейнера с использованием образа Docker Hub**:

```bash
docker run -d \
  -p 9155:9155 \
  -v ./config.yaml:/app/config.yaml \
  docker.io/gizex/tuya-smartplug-exporter:latest
```

Этот командный запуск создаст контейнер, который будет слушать порт `9155` и монтировать файл конфигурации `config.yaml` из локальной директории на хосте в контейнер.

- `-p 9155:9155` — пробрасывает порт `9155`, чтобы Prometheus мог собирать метрики.
- `-v ./config.yaml:/app/config.yaml` — монтирует файл конфигурации с настройками устройств.

#### Пример содержимого `config.yaml`:

```yaml
- name: "socket-2-prxmx-2"
  id: "your-device-id"
  key: "your-device-key"
  ip: "192.168.1.100"
  protocol: "v3.3"

- name: "socket-4-prxmx-1"
  id: "your-device-id"
  key: "your-device-key"
  ip: "192.168.1.101"
  protocol: "v3.4"
```

### 2. С использованием Docker Compose

Если ты хочешь использовать `docker-compose` для упрощения процесса развертывания, создавай файл `docker-compose.yml` с таким содержимым:

```yaml
version: '3.8'

services:
  tuya-smartplug-exporter:
    image: docker.io/gizex/tuya-smartplug-exporter:latest
    container_name: tuya-smartplug-exporter
    ports:
      - "9155:9155"
    volumes:
      - ./config.yaml:/app/config.yaml
    restart: always
    environment:
      - TZ=Europe/Moscow  # Устанавливаем временную зону
```

После этого ты можешь запустить проект с помощью команды:

```bash
docker-compose up -d
```

Контейнер будет автоматически перезапускаться при сбоях и использовать конфигурацию из файла `config.yaml`.

### 3. Локальная сборка Docker-образа

Если ты хочешь собрать образ самостоятельно, используй следующий `Dockerfile`:

```dockerfile
# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для Prometheus
EXPOSE 9155

# Запускаем приложение
CMD ["python", "main.py"]
```

Затем собери образ:

```bash
docker build -t gizex/tuya-smartplug-exporter:latest .
```

И запусти его:

```bash
docker run -d -p 9155:9155 -v ./config.yaml:/app/config.yaml gizex/tuya-smartplug-exporter:latest
```

## Метрики

Экспортер публикует следующие метрики:

- `tuya_smartplug_power` — общая мощность, используемая устройством, в ваттах.
- `tuya_smartplug_voltage` — напряжение устройства в вольтах.
- `tuya_smartplug_current` — ток устройства в миллиамперах.
- `tuya_smartplug_switch_on` — состояние устройства (1 для включенного, 0 для выключенного).
- `tuya_smartplug_power_kwh_day` — проекция потребления энергии на день в кВт·ч.

## Конфигурация

Конфигурация устройств хранится в файле `config.yaml`, где каждый объект описывает одно устройство Tuya. Пример конфигурации:

```yaml
- name: "socket-2-prxmx-2"
  id: "your-device-id"
  key: "your-device-key"
  ip: "192.168.1.100"
  protocol: "v3.3"

- name: "socket-4-prxmx-1"
  id: "your-device-id"
  key: "your-device-key"
  ip: "192.168.1.101"
  protocol: "v3.4"
```

- `name`: Имя устройства (можно использовать для меток в Prometheus).
- `id`: Идентификатор устройства (получается через Tuya API).
- `key`: Ключ устройства (получается через Tuya API).
- `ip`: IP-адрес устройства.
- `protocol`: Протокол для связи (например, `v3.4`).

## Примечания

- Убедись, что все устройства, указанные в конфигурации, доступны по сети и правильно настроены.
- По умолчанию экспортер будет собирать данные каждую секунду, но это можно настроить в самом коде, если необходимо.

## Логирование

Приложение выводит логи в консоль с использованием стандартного Python логирования, чтобы отслеживать состояние и ошибки. Вы можете изменить уровень логирования в коде, если хотите получать более подробную информацию.
