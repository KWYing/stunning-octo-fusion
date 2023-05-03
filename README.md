# stunning-octo-fusion
info control

---

## Running server using uvicorn

1. Create a new serive file in systemd
```
sudo nano /etc/systemd/system/[nameofservice]
```

2. Enter this into the file
```
[Unit]
Description=Info about your app
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/file/path/of/your/app
ExecStart=/file/path/to/venv/bin/uvicorn main:app --host=0.0.0.0 --port=8000

[Install]
WantedBy=multi-user.target
```
Then `ctrl+x` to save and exit.


3. Start the service using
```
sudo systemctl start [appServiceName]
sudo systemctl enable [appSericeName]
```

4. Stop the service using
```
sudo systemctl stop [appServiceName]