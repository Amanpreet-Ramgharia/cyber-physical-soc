# Raspberry Pi Setup (Bookworm / Debian 12)

## GPIO Summary
- DHT11 data: GPIO5
- PIR OUT: GPIO17
- MPU6050 software I2C: SDA GPIO21, SCL GPIO20

## Install dependencies
```bash
sudo apt update
sudo apt install -y python3-venv python3-smbus i2c-tools
```

## Python venv
```bash
python3 -m venv ~/iot-venv --system-site-packages
source ~/iot-venv/bin/activate
pip install -r requirements.txt
```

## Software I2C (MPU6050)

1) Edit `/boot/firmware/config.txt`:
```bash
sudo nano /boot/firmware/config.txt
```

2) Add (example):
```ini
dtoverlay=i2c-gpio,i2c_gpio_sda=21,i2c_gpio_scl=20,bus=3
```

3) Reboot:
```bash
sudo reboot
```

4) Verify bus exists:
```bash
ls -l /dev/i2c-*
sudo i2cdetect -y 3
```

If you see `68` or `69`, update `I2C_BUS` / `ADDRESS` in `sensors/mpu6050_to_jsonl.py`.
