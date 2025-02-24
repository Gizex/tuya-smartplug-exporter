Here is the updated **README** in English, including the usage of the `docker.io/gizex/tuya-smartplug-exporter:latest` Docker image:

---

# Tuya SmartPlug Exporter

This project is an exporter for integrating with Prometheus, which collects metrics from Tuya smart plugs using their API. The exporter collects information about power, current, voltage, and device state, and also calculates the projected energy consumption in kWh per day.

## Installation

### 1. Using Docker

The easiest way to run the exporter is to use Docker. We provide a ready-made image that you can pull from Docker Hub.

#### Running with Docker

1. **Run the container using the Docker Hub image**:

```bash
docker run -d \
  -p 9155:9155 \
  -v ./config.yaml:/app/config.yaml \
  docker.io/gizex/tuya-smartplug-exporter:latest
```

This command will create a container that listens on port `9155` and mounts the `config.yaml` configuration file from your local directory.

- `-p 9155:9155` — exposes port `9155`, allowing Prometheus to scrape metrics.
- `-v ./config.yaml:/app/config.yaml` — mounts the configuration file containing device settings.

#### Example `config.yaml` content:

```yaml
- name: "socket-2-prxmx-2"
  id: "your-device-id"
  key: "your-device-key"
  ip: "192.168.1.100"
  protocol: "v1.0"

- name: "socket-4-prxmx-1"
  id: "your-device-id"
  key: "your-device-key"
  ip: "192.168.1.101"
  protocol: "v1.0"
```

### 2. Using Docker Compose

If you prefer to use `docker-compose` to simplify the deployment, create a `docker-compose.yml` file with the following content:

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
      - TZ=Europe/Moscow  # Set the timezone
```

After that, you can start the project with:

```bash
docker-compose up -d
```

This will automatically restart the container if it crashes and use the configuration from the `config.yaml` file.

### 3. Building the Docker Image Locally

If you'd like to build the image yourself, here’s the `Dockerfile`:

```dockerfile
# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Prometheus
EXPOSE 9155

# Run the application
CMD ["python", "tuya_exporter.py"]
```

Then, build the image:

```bash
docker build -t gizex/tuya-smartplug-exporter:latest .
```

And run it:

```bash
docker run -d -p 9155:9155 -v ./config.yaml:/app/config.yaml gizex/tuya-smartplug-exporter:latest
```

## Metrics

The exporter exposes the following metrics:

- `tuya_smartplug_power` — total power used by the device in watts.
- `tuya_smartplug_voltage` — the device voltage in volts.
- `tuya_smartplug_current` — the device current in milliamps.
- `tuya_smartplug_switch_on` — device state (1 for on, 0 for off).
- `tuya_smartplug_power_kwh_day` — projected energy consumption per day in kWh.

## Configuration

Device configuration is stored in the `config.yaml` file, where each object describes a Tuya device. Example configuration:

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

- `name`: The name of the device (used as labels in Prometheus).
- `id`: The device ID (obtained via Tuya API).
- `key`: The device key (obtained via Tuya API).
- `ip`: The device IP address.
- `protocol`: The protocol for communication (e.g., `v3.4`).

## Notes

- Ensure that all devices listed in the configuration file are accessible on the network and properly set up.
- By default, the exporter will collect data every second, but this can be adjusted in the code if necessary.

## Logging

The application logs to the console using Python’s standard logging module to track the state and errors. You can change the logging level in the code if you need more detailed information.

---

With this updated README, setting up and running the project with Docker or Docker Compose should be easier.