#

# gcastilloh@DevSys:/etc/systemd/system$ cat midemonio.service
```

[Unit]
Description=Inicia demonio
After=network.target

[Service]
ExecStart=/var/www/proyectosdjango/Describeme/iniciademonio.sh
Restart=always
WorkingDirectory=/var/www/proyectosdjango
User=fjimenezh
Group=www-data
StartLimitBurst=0

[Install]
WantedBy=multi-user.target
gcastilloh@DevSys:/etc/systemd/system$ ^C
gcastilloh@DevSys:/etc/systemd/system$ sudo systemctl daemon-reload
gcastilloh@DevSys:/etc/systemd/system$ cat midemonio.service
[Unit]
Description=Inicia demonio
After=network.target

[Service]
ExecStart=/var/www/proyectosdjango/Describeme/iniciademonio.sh
Restart=always
WorkingDirectory=/var/www/proyectosdjango
User=fjimenezh
Group=www-data
StartLimitBurst=0

[Install]
WantedBy=multi-user.target

```
