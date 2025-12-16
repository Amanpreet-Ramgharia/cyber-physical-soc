# systemd Services

Copy the `.service` files to:
`/etc/systemd/system/`

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cp-soc-dht11.service
sudo systemctl enable --now cp-soc-pir.service
sudo systemctl enable --now cp-soc-mpu6050.service
```

Check logs:
```bash
sudo journalctl -u cp-soc-dht11.service -f
```
