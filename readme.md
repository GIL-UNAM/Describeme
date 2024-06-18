# Introducción

Describe está interado por dos sistemas:

* el frontend implementado en django, que permite alimentar una consulta al sistema y mostrar los resultados, todo via web. 
* el backend que corresponde a la aplicación propiamente dicha y que se implementa por medio de un servicio via sockets

## Backend

El backend está constituido por los siguientes archivos localizados dentro del directorio ./descriemeapp:

server.py
defineme_eng.py
defineme_esp.py
bitacora.py

## Frontend

Es una app django que se localiza en el directorio ./describemeapp 

El front no tiene modelos definidos y todo el funcionamiento está colocado directamente en el archivo views.py mientras que los templates se localizan en el directorio ./describespp/templates

## Backend

El backend, es un servicio que debe levantarse y es independiente del formtend por lo que se ha creado un script que inicia el servicio en el servidor. A continuación se muestra el contenido del sevicio (midemonio.service) y que deb activarse en el servidor... 

### /etc/systemd/system/midemonio.service

```shell

[Unit]
Description=Inicia demonio
After=network.target

[Service]
ExecStart=/var/www/Describeme/iniciademonio.sh
Restart=always
WorkingDirectory=/var/www/
User=usuario
Group=www-data
StartLimitBurst=0

[Install]
WantedBy=multi-user.target
```

## Posibles mejoras

* No usar django como frontend, si se cambia de lenguaje entonces se tendría que mantener el servidor y su servicio
* si se mantiene python, pdria emplearse un framework mas ligero, por ejemplo flask e integrar el servidor en el código para evitar mantener un servicio activo siempre
